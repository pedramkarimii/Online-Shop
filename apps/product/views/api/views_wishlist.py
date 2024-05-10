import json
from django.http import JsonResponse
from rest_framework.response import Response
from apps.product.form_data import forms
from rest_framework import status, views
from django.shortcuts import get_object_or_404
from django.core.signing import Signer
from apps.product.form_data import serializers


class WishlistAddProductAPI(views.APIView):
    def dispatch(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(serializers.Product, pk=kwargs['pk'])  # noqa
        self.signer = Signer()  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.signed_product_id = self.signer.sign(str(self.product_instance.pk))  # noqa
        self.latest_discount = self.product_instance.product_code_discounts.filter(is_expired=False).order_by(  # noqa
            '-create_time').first()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.user_authenticated:
            return self.add_product_to_wishlist_cookie()
        return self.add_product_to_wishlist_authenticated()

    def add_product_to_wishlist_cookie(self):
        product_discount = self.calculate_product_discount()

        cookie_key = f"product_{self.signed_product_id}"
        if cookie_key not in self.request.COOKIES:
            product_data = {
                'product': self.product_instance.pk,
                'defaults': {
                    'quantity': 1,
                    'total_price': product_discount if product_discount else self.product_instance.price
                }
            }
            product_json = json.dumps(product_data)
            response = Response({
                "message": f"Product added to wishlist successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(cookie_key, product_json, max_age=604800)
            return response
        else:
            return self.add_exist_product_to_wishlist_cookie(self.signed_product_id, product_discount)

    def add_exist_product_to_wishlist_cookie(self, signed_product_id, product_discount):
        cookie_key = f"product_{signed_product_id}"
        if cookie_key in self.request.COOKIES:
            product_data = json.loads(self.request.COOKIES[cookie_key])
            product_id = product_data.get('product')
            quantity = product_data.get('quantity', 0)
            total_price = product_data.get('total_price', 0)
            if product_discount is not None:
                total_price += product_discount
            elif product_discount is None and total_price is None:
                total_price += self.product_instance.price
            elif product_discount is None and total_price is not None:
                total_price += self.product_instance.price
            quantity += 1
            new_product_data = {
                "product": product_id,
                "quantity": quantity,
                "total_price": total_price
            }
            response = Response(new_product_data, status=status.HTTP_200_OK)
            response.set_cookie(cookie_key, json.dumps(new_product_data), max_age=604800)
            return response

    def add_product_to_wishlist_authenticated(self):
        product_discount = self.calculate_product_discount()
        wishlist, created = forms.Wishlist.objects.get_or_create(
            user=self.request.user,
            product=self.product_instance,
            defaults={'quantity': 1,
                      'total_price': product_discount if product_discount else self.product_instance.price}
        )
        if not created:
            wishlist.quantity += 1
            wishlist.total_price += product_discount if product_discount else self.product_instance.price
            wishlist.save()
        else:
            wishlist.save()
        serializer = serializers.WishlistProductSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def calculate_product_discount(self):
        product_price = self.product_instance.price
        if not self.latest_discount:
            return None
        numerical_discount = self.latest_discount.numerical_discount
        percentage_discount = self.latest_discount.percentage_discount
        if numerical_discount and percentage_discount:
            product_numerical_discount = product_price - numerical_discount
            product_percentage_discount = product_price - (product_price * percentage_discount / 100)
            if product_numerical_discount < product_percentage_discount:
                return product_numerical_discount
            else:
                return product_percentage_discount
        elif percentage_discount:
            return product_price - (product_price * percentage_discount / 100)
        elif numerical_discount:
            return product_price - numerical_discount
        return None


class WishlistShowProductAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.show_product_from_wishlist_cookie(request)
        return self.show_product_from_wishlist_authenticated(request)

    # @staticmethod
    def show_product_from_wishlist_cookie(self, request):  # noqa
        wishlist_data = {}
        for key, value in request.COOKIES.items():
            if key.startswith('product_'):
                product_data = json.loads(value)
                wishlist_data[key] = product_data
        return JsonResponse(wishlist_data, status=status.HTTP_200_OK)

#     @staticmethod
    def show_product_from_wishlist_authenticated(self, request): # noqa
        wishlist_items = forms.Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishlistProductSerializer(wishlist_items, many=True)
        return JsonResponse(serializer.data, safe=False)
