from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.account.models import CodeDiscount, Role, Address
from apps.order.form_data import forms
from apps.order import mixin


class AddOrderView(mixin.ProductDiscountMixin):
    """
    Class-base view for add order
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):  # noqa
        """
        Function for setup data to view
        """
        super().setup(request, *args, **kwargs)
        self.next_page_payment_order = reverse_lazy('payment_order')  # noqa
        self.template_order = 'order/order/add_order.html'  # noqa
        self.user_is_authenticated = request.user.is_authenticated  # noqa
        self.user = request.user  # noqa
        self.user_id = request.user.id  # noqa

        self.code_discounts_role = CodeDiscount.objects.filter(  # noqa
            is_expired=False,
            is_active=True
        ).order_by('-create_time').first()
        self.latest_discount = self.code_discounts_role.code  # noqa
        self.user_has_discount = Role.objects.filter(  # noqa
            code_discount__code=self.latest_discount,
            is_deleted=False,
            is_active=True
        ).filter(
            Q(golden=self.user_id) | Q(silver=self.user_id) | Q(bronze=self.user_id) | Q(
                seller=self.user_id)
        ).exists()
        self.form_class = forms.OrderForm  # noqa

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests: instantiate a blank version of the form.
        """
        order_item = forms.OrderItem.objects.filter(user=self.user)  # noqa
        cart_data = {}
        sum_total_price = 0
        pk_product = None
        for item in order_item:
            total = item.product.price * item.quantity
            product = item.product  # noqa
            pk_product = product.pk
            sum_total_price += item.total_price
            latest_discount_product_price = product.product_code_discounts.filter(is_expired=False,
                                                                                  is_active=True).order_by(
                '-create_time').first()
            product_discount = self.calculate_product_discount(product_instance=product,
                                                               latest_discount=latest_discount_product_price)
            cart_data[item.product.pk] = {
                'product': item.product.id,
                'image_url': product,
                'name': item.product.name,
                'price': product_discount if product_discount else product.price,
                'quantity': item.quantity,
                'total': total,
                'total_price': item.total_price,
            }
        form = self.form_class()
        form.fields['address'].queryset = Address.objects.filter(user=self.user)
        return render(self.request, self.template_order,
                      {'form': form, 'pk_product': pk_product, 'products': cart_data,
                       'sum_total_price': sum_total_price})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        """
        form = self.form_class(self.request_post)
        if form.is_valid() and self.user_is_authenticated:
            return self.process_order(form)
        return JsonResponse({'success': False, 'message': _('You must be logged in to place an order')})

    def process_order(self, form):
        """
        function to process the order and save it to the database.
        """
        order_items = forms.OrderItem.objects.filter(user=self.user)
        order = form.save(commit=False)
        product_discount = form.cleaned_data.get('finally_price')
        if self.user_has_discount:
            product_discount = self.calculate_product_discount(form.cleaned_data.get('finally_price'),
                                                               self.code_discounts_role)
        order.product = self.product_instance
        order.product_discount = product_discount

        if self.user_is_authenticated:
            order.user = self.request.user
            order.address = form.cleaned_data.get('address')
            order.finally_price = product_discount
            order.save()
            order.order_item.set(order_items)
            order.save()
            response = JsonResponse({'success': True, 'message': _('Order added successfully')})
            return redirect(self.next_page_payment_order)
        else:
            response = JsonResponse({'success': False, 'message': _('You must be logged in to place an order')})

        return response
