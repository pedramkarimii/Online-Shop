from django.core.signing import Signer
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from apps.order.form_data import forms
from apps.order import mixin


class AddOrderView(mixin.ProductDiscountMixin):
    def setup(self, request, *args, **kwargs):
        self.signer = Signer()  # noqa
        self.template_order = 'order/order/add_order.html'  # noqa
        self.user_is_authenticated = request.user.is_authenticated  # noqa
        self.user = request.user  # noqa
        self.form_class = forms.OrderForm  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        order_item = forms.OrderItem.objects.filter(user=self.user)  # noqa
        cart_data = {}
        sum_total_price = 0
        pk_product = None
        for item in order_item:
            total = item.product.price * item.quantity
            product = item.product
            pk_product = product.pk
            sum_total_price += item.total_price
            latest_discount_product_price = product.product_code_discounts.filter(is_expired=False,
                                                                                  is_active=True).order_by(
                '-create_time').first()
            calculate = mixin.ProductDiscountMixin()
            product_discount = calculate.calculate_product_discount(product_instance=product,
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

        return render(self.request, self.template_order,
                      {'form': self.form_class(), 'pk_product': pk_product, 'products': cart_data,
                       'sum_total_price': sum_total_price})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post)
        if form.is_valid() and self.user_is_authenticated:
            return self.process_order(form)
        return JsonResponse({'success': False, 'message': _('You must be logged in to place an order')})

    def process_order(self, form):
        order_items = forms.OrderItem.objects.filter(user=self.user)
        product_discount = self.calculate_product_discount(self.product_instance, form.cleaned_data.get('quantity'))
        order = form.save(commit=False)
        order.product = self.product_instance
        order.product_discount = product_discount

        if self.user_is_authenticated:
            order.user = self.request.user
            order.address = form.cleaned_data.get('address')
            order.finally_price = form.cleaned_data.get('finally_price')
            order.save()
            order.order_item.set(order_items)
            order.save()
            response = JsonResponse({'success': True, 'message': _('Order added successfully')})
        else:
            response = JsonResponse({'success': False, 'message': _('You must be logged in to place an order')})

        return response
