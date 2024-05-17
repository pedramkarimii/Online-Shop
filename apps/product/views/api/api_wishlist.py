import json
from django.http import JsonResponse
from rest_framework.response import Response
from apps.product.form_data import forms
from rest_framework import status, views
from apps.product.form_data import serializers
from django.utils.translation import gettext_lazy as _
from apps.product import mixin


class WishlistAddProductAPI(views.APIView, mixin.ProductDiscountMixin):

    def add_product_to_wishlist_authenticated(self):
        product_discount = self.calculate_product_discount(self.product_instance, self.latest_discount)
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


class WishlistShowProductAPI(views.APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.show_product_from_wishlist_cookie(request)
        return self.show_product_from_wishlist_authenticated(request)

    def show_product_from_wishlist_cookie(self, request):  # noqa
        wishlist_data = {}
        for key, value in request.COOKIES.items():
            if key.startswith('product_'):
                product_data = json.loads(value)
                wishlist_data[key] = product_data
        return JsonResponse(wishlist_data, status=status.HTTP_200_OK)

    def show_product_from_wishlist_authenticated(self, request):  # noqa
        wishlist_items = forms.Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishlistProductSerializer(wishlist_items, many=True)
        return JsonResponse(serializer.data, safe=False)
