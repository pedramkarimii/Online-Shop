import json
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views import generic
from apps.product.form_data import forms
from django.core.signing import Signer

from apps.product import mixin
from apps.product.mixin import ProductDiscountMixin


class WishlistAddProductView(mixin.ProductDiscountMixin):

    def add_product_to_wishlist_authenticated(self):
        # form = self.form_class(self.request_post)
        # if form.is_valid():  # noqa
        product_discount = self.calculate_product_discount(self.product_instance, self.latest_discount)  # noqa
        wishlist, created = forms.Wishlist.objects.get_or_create(
            user=self.request.user,
            product=self.product_instance,
            quantity=1,
            total_price=product_discount if product_discount else self.product_instance.price
        )
        if not created:
            wishlist.quantity += 1
            wishlist.total_price += product_discount if product_discount else self.product_instance.price
            wishlist.save()

        else:
            wishlist.save()
        response = JsonResponse({'message': _('Product added to wishlist successfully.')})
        return response


class WishlistShowProductView(generic.ListView):
    def get(self, request, *args, **kwargs):  # noqa
        if not request.user.is_authenticated:
            return self.show_product_from_wishlist_cookie(request)
        return self.show_product_from_wishlist_authenticated(request)

    def show_product_from_wishlist_cookie(self, request):  # noqa
        wishlist_items_cookies = {}
        sum_total_price = 0
        img_url = set()
        for key, value in request.COOKIES.items():
            if key.startswith('product_'):
                product_data = json.loads(value)
                wishlist_items_cookies[key] = product_data
                total_price = product_data.get('total_price', 0)
                sum_total_price += total_price
                product_id = product_data.get('product')
                product_instance = forms.Product.objects.get(pk=product_id)
                media_instances = product_instance.media_products.all()
                for media_instance in media_instances:
                    url = media_instance.get_img()
                    img_url.add(url)

        return render(request, 'product/wishlist/wishlist.html',
                      {'img_url': img_url, 'wishlist_items_cookies': wishlist_items_cookies,
                       'sum_total_price': sum_total_price})

    def show_product_from_wishlist_authenticated(self, request):  # noqa
        wishlist_items = forms.Wishlist.objects.filter(user=request.user)
        wishlist_data = {}
        sum_total_price = 0
        pk_product = None
        for item in wishlist_items:
            product = item.product
            pk_product = product.pk
            sum_total_price += item.total_price
            latest_discount_product_price = product.product_code_discounts.filter(is_expired=False,
                                                                                  is_active=True).order_by(
                '-create_time').first()
            calculate = ProductDiscountMixin()
            product_discount = calculate.calculate_product_discount(product_instance=product,
                                                                    latest_discount=latest_discount_product_price)
            wishlist_data[item.product.pk] = {
                'product': item.product.id,
                'image_url': product,
                'name': item.product.name,
                'price': product_discount if product_discount else product.price,
                'quantity': item.quantity,
                'total_price': item.total_price,
            }
        return render(request, 'product/wishlist/wishlist.html',
                      {'pk_product': pk_product, 'wishlist_items': wishlist_data, 'sum_total_price': sum_total_price})


class WishlistUpdateProductView(WishlistAddProductView):
    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""  # noqa
        self.product_instance = get_object_or_404(forms.Product, pk=kwargs['pk'])  # noqa
        self.signer = Signer()  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.signed_product_id = self.signer.sign(str(self.product_instance.pk))  # noqa
        self.latest_discount = self.product_instance.product_code_discounts.filter(is_expired=False,  # noqa
                                                                                   is_active=True).order_by(
            '-create_time').first()
        self.request_quantity = request.POST.get('quantity')  # noqa
        self.request_total_price = request.POST.get('total_price')  # noqa
        self.form_class = forms.WishlistAddForm  # noqa
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # noqa
        if not request.user.is_authenticated:
            return self.update_product_from_wishlist_cookie(request)
        else:
            return self.update_product_from_wishlist_authenticated(request)

    def update_product_from_wishlist_authenticated(self, request):

        if self.user_authenticated:
            new_quantity = int(self.request_quantity)
            new_total_price = int(self.request_total_price)
            product = self.product_instance
            with transaction.atomic():
                wishlist_qs = forms.Wishlist.objects.get(user=request.user, product=product)
                wishlist_qs.quantity = new_quantity
                wishlist_qs.total_price = new_total_price
                wishlist_qs.save()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    def update_product_from_wishlist_cookie(self, request):
        new_quantity = int(self.request_quantity)
        new_total_price = int(self.request_total_price)

        product_discount = self.calculate_product_discount(self.product_instance, self.latest_discount)
        cookie_key = f"product_{self.signed_product_id}"
        if cookie_key in self.request.COOKIES:
            # product_data = json.loads(request.COOKIES[cookie_key])
            product_data = {
                'product': self.product_instance.pk,
                'name': self.product_instance.name,
                'price': product_discount if product_discount else self.product_instance.price,
                'quantity': new_quantity,
                'total_price': new_total_price
            }

            product_json = json.dumps(product_data)
            response = JsonResponse({'success': True})
            response.set_cookie(cookie_key, product_json, max_age=604800)
        else:
            response = JsonResponse({'success': False})

        return response
