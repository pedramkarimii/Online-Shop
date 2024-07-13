import json
from django.core.signing import Signer
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from apps.account.models import UserAuth, Role, CodeDiscount
from apps.account.users_auth.authenticate import JWTAuthentication
from apps.account.users_auth.services import update_user_auth_uuid
from apps.product.form_data import forms
from rest_framework import status, views
from apps.product.form_data import serializers
from apps.product import mixin
from apps.product.mixin import ProductDiscountMixin


class WishlistAddProductAPI(views.APIView, mixin.ProductDiscountMixin):
    """
    class for adding products to wishlist.
    if the user is not authenticated, it will add the product to the wishlist cookie.
    if the user is authenticated, it will add the product to the wishlist model.
    """

    def add_product_to_wishlist_authenticated(self):
        """
        function for adding product to wishlist authenticated user.
        :return: JsonResponse with serialized wishlist data.
        """
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
    """
    class for showing products in wishlist.
    if the user is not authenticated, it will show the product from the wishlist cookie.
    if the user is authenticated, it will show the product from the wishlist model.
    """
    def get(self, request, *args, **kwargs):
        """
        function for showing product in wishlist.
        :param request: HttpRequest object.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: JsonResponse with serialized wishlist data.
        """
        if not request.user.is_authenticated:
            return self.show_product_from_wishlist_cookie(request)
        return self.show_product_from_wishlist_authenticated(request)

    def show_product_from_wishlist_cookie(self, request):  # noqa
        """
        function for showing product from wishlist cookie.
        :param request: HttpRequest object.
        :return: JsonResponse with serialized wishlist data.
        """
        wishlist_data = {}
        for key, value in request.COOKIES.items():
            if key.startswith('product_wishlist'):
                product_data = json.loads(value)
                wishlist_data[key] = product_data
        return JsonResponse(wishlist_data, status=status.HTTP_200_OK)

    def show_product_from_wishlist_authenticated(self, request):  # noqa
        """
        function for showing product from wishlist authenticated user.
        :param request: HttpRequest object.
        :return: JsonResponse with serialized wishlist data.
        """
        wishlist_items = forms.Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishlistProductSerializer(wishlist_items, many=True)
        return JsonResponse(serializer.data, safe=False)


class WishlistUpdateProductAPI(views.APIView):
    """
    class for updating products in wishlist.
    if the user is not authenticated, it will update the product from the wishlist cookie.
    if the user is authenticated, it will update the product from the wishlist model.
    """
    def setup(self, request, *args, **kwargs):
        """
        function for setting up the view.
        :param request: HttpRequest object.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: None.
        """
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

    def post(self, request, *args, **kwargs):
        """
        function for updating product in wishlist.
        :param request: HttpRequest object.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: JsonResponse with serialized wishlist data.
        """
        if not request.user.is_authenticated:
            return self.update_product_from_wishlist_cookie(request)

        return self.update_product_from_wishlist_authenticated(request)

    def update_product_from_wishlist_cookie(self, request):  # noqa
        """
        function for updating product from wishlist cookie.
        :param request: HttpRequest object.
        :return: JsonResponse with serialized wishlist data.
        """
        new_quantity = int(self.request_quantity)
        new_total_price = int(self.request_total_price)
        calculate = ProductDiscountMixin()
        product_discount = calculate.calculate_product_discount(self.product_instance, self.latest_discount)
        cookie_key = f"product_wishlist{self.signed_product_id}"
        if cookie_key in self.request.COOKIES:
            product_data = {
                'product': self.product_instance.pk,
                'name': self.product_instance.name,
                'price': product_discount if product_discount else self.product_instance.price,
                'quantity': new_quantity,
                'total_price': new_total_price
            }
            print(product_data)

            product_json = json.dumps(product_data)
            print(product_json)
            response = JsonResponse({'success': True})
            response.set_cookie(cookie_key, product_json, max_age=604800)
            response.status_code = status.HTTP_200_OK
        else:
            response = JsonResponse({'success': False})
            response.status_code = status.HTTP_404_NOT_FOUND

        return response

    def update_product_from_wishlist_authenticated(self, request):  # noqa
        """
        function for updating product
        """
        wishlist_items = forms.Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishlistProductSerializer(wishlist_items, many=True)
        return JsonResponse(serializer.data, safe=False)


class WishlistDeleteProductAPI(views.APIView):
    """
    class for deleting products in wishlist.
    """
    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""  # noqa
        self.product_instance = get_object_or_404(forms.Product, pk=kwargs['pk'])  # noqa
        self.signer = Signer()  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.signed_product_id = self.signer.sign(str(self.product_instance.pk))  # noqa
        return super().setup(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):  # noqa
        """
        function for deleting product in wishlist.
        if the user is not authenticated, it will delete the product from the wishlist cookie.
        if the user is authenticated, it will delete the product from the wishlist model.
        """
        if not request.user.is_authenticated:
            return self.delete_product_from_wishlist_cookie(request)

        return self.delete_product_from_wishlist_authenticated(request)

    def delete_product_from_wishlist_cookie(self, request):
        """
        function for deleting product from wishlist cookie.
        :param request: HttpRequest object.
        :return: JsonResponse with success message.
        """
        cookie_key = f"product_wishlist{self.signed_product_id}"
        if cookie_key in request.COOKIES:

            response = JsonResponse({'success': True})
            response.delete_cookie(cookie_key)
        else:
            response = JsonResponse({'success': False})
        return response

    def delete_product_from_wishlist_authenticated(self, request):  # noqa
        """
        function for deleting product from wishlist authenticated user.
        if the user is authenticated, it will delete the product from the wishlist model.
        :param request: HttpRequest object.
        :return: JsonResponse with success message.
        """
        product = self.product_instance
        if self.user_authenticated:
            with transaction.atomic():
                wishlist_obj = forms.Wishlist.objects.filter(user=request.user, product=product).first()
                wishlist_obj.delete()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


class WishlistDiscountCodProductAPI(views.APIView):
    """
    class for discounting products in wishlist.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""  # noqa
        print(*[f'{k} : {v}' for k, v in request.META.items()], sep='\n')
        self.user_instance = request.user.id  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.code_discounts_role = CodeDiscount.objects.filter(  # noqa
            is_expired=False,
            is_active=True
        ).order_by('-create_time').first()
        self.request_code_discount = request.POST.get('code_discount')  # noqa
        self.request_total_price = request.POST.get('total_price')  # noqa
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        function for discounting product in wishlist.
        if the user is authenticated, it will discount the product from the wishlist model.
        :param request: HttpRequest object.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: JsonResponse with success message.
        """
        if self.user_authenticated:
            print(f'User authenticated: {self.user_authenticated}')  # Debugging line
            print(f'User instance: {self.user_instance}')  # Debugging line
            print(*[f'{k} : {v}' for k, v in request.META.items()], sep='\n')
            return self.discount_cod_product_from_wishlist_cookie(request)
        else:
            print(f'User authenticated: {self.user_authenticated}')  # Debugging line
            print(f'User instance: {self.user_instance}')  # Debugging line
            print(*[f'{k} : {v}' for k, v in request.META.items()], sep='\n')
            return JsonResponse({'success': False, 'message': 'User not authenticated'},
                                status=status.HTTP_401_UNAUTHORIZED)

    def discount_cod_product_from_wishlist_cookie(self, request):
        """
        function for discounting product from wishlist cookie.
        if the user is authenticated, it will discount the product from the wishlist model.
        :param request: HttpRequest object.
        :return: JsonResponse with success message.
        """
        code_discount = self.code_discounts_role.code
        user_has_discount = Role.objects.filter(
            code_discount__code=code_discount,
            is_deleted=False,
            is_active=True
        ).filter(
            Q(golden=self.user_instance) | Q(silver=self.user_instance) | Q(bronze=self.user_instance) | Q(
                seller=self.user_instance)
        ).exists()

        if user_has_discount and code_discount == self.request_code_discount:
            new_total_price = int(self.request_total_price)
            calculate = ProductDiscountMixin()
            product_discount = calculate.calculate_product_discount(new_total_price, self.code_discounts_role)
            wishlist_qs = forms.Wishlist.objects.filter(user=self.user_instance).first()

            if wishlist_qs:
                with transaction.atomic():
                    wishlist_qs.total_price = product_discount
                    wishlist_qs.save()
                    return JsonResponse({'success': True}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'success': False, 'message': 'Wishlist not found'},
                                    status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'success': False, 'message': 'Discount not applicable or invalid code'},
                                status=status.HTTP_400_BAD_REQUEST)

