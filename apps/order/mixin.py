import json
from django.core.signing import Signer
from django.shortcuts import get_object_or_404
from apps.order.form_data import forms
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from apps.product.models import Product


class ProductDiscountMixin(generic.View):
    """
    Defines a mixin class that provides methods for handling product discounts and adding products to
     the shopping cart.
    """

    def setup(self, request, *args, **kwargs):
        """
        Initializes necessary variables and retrieves the product instance based on the URL parameter
        `pk`. Uses the `Signer` to sign the product ID for secure retrieval. Also retrieves the
         latest discount applicable to the product and initializes form data for processing.
        """

        self.product_instance = get_object_or_404(Product, pk=kwargs['pk'])  # noqa
        self.signer = Signer()  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.signed_product_id = self.signer.sign(str(self.product_instance.pk))  # noqa
        self.latest_discount = self.product_instance.product_code_discounts.filter(is_expired=False,  # noqa
                                                                                   is_active=True).order_by(
            '-create_time').first()
        self.request_post = request.POST  # noqa
        self.form_class = forms.OrderItemForm  # noqa
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests. If the user is not authenticated, calls a method to add the product
        to the cart stored in cookies. Otherwise, adds products from cookies to the cart for
        authenticated users.
        """

        if not self.user_authenticated:
            return self.add_product_to_cart_cookie()
        else:
            return self.add_products_from_cookies_to_cart_authenticated()

    def add_products_from_cookies_to_cart_authenticated(self):
        """
        Adds products to the cart for authenticated users based on product data stored in cookies.
         Handles exceptions and deletes cookies if products do not exist. Prepares a response
         after adding products, including deleting cookies that were processed.
        """

        cookies_to_delete = []
        if self.request.session and any(key.startswith("product_cart") for key in self.request.COOKIES):
            for cookie_key, cookie_value in self.request.COOKIES.items():  # noqa
                if cookie_key.startswith("product_cart"):
                    product_data = json.loads(cookie_value)
                    product_id = product_data.get('product')
                    quantity = product_data.get('quantity', 0)
                    total_price = product_data.get('total_price', 0)
                    try:
                        self.add_cookie_product_to_cart_get_or_create(product_id, quantity,
                                                                      total_price, cookie_key,
                                                                      cookies_to_delete)
                    except Exception:  # noqa
                        response = JsonResponse({'message': _('Product Does Not Exist.')})
                        response.delete_cookie(cookie_key)
                        continue
            response = self.prepare_response_after_adding_products(cookies_to_delete)
        else:
            response = self.add_product_to_cart_authenticated()
        return response

    def add_product_to_cart_cookie(self):
        """
        Adds a product to the cart stored in cookies if it doesn't already exist. Otherwise,
         calls a method to update an existing product in the cookie-based cart.
        """

        product_discount = self.calculate_product_discount(self.product_instance, self.latest_discount)
        cookie_key = f"product_cart{self.signed_product_id}"
        if cookie_key not in self.request.COOKIES:
            product_data = {
                'product': self.product_instance.pk,
                'name': self.product_instance.name,
                'price': self.product_instance.price,
                'quantity': 1,
                'total_price': product_discount if product_discount else self.product_instance.price
            }
            product_json = json.dumps(product_data)

            response = JsonResponse({'message': _('Product added to cart successfully.')})
            response.set_cookie(cookie_key, product_json, max_age=604800)
            return response
        else:

            return self.add_exist_product_to_cart_cookie(self.signed_product_id, product_discount)

    def add_exist_product_to_cart_cookie(self, signed_product_id, product_discount):
        """
        Updates an existing product in the cart stored in cookies by incrementing its quantity and
        recalculating the total price.
        """

        cookie_key = f"product_cart{signed_product_id}"
        if cookie_key in self.request.COOKIES:
            product_data = json.loads(self.request.COOKIES[cookie_key])  # noqa
            product_id = product_data.get('product')
            name = product_data.get('name')
            price_id = product_data.get('price')
            quantity = product_data.get('quantity', 0)
            total_price = product_data.get('total_price', 0)
            total_price = self.calculate_total_price(product_discount, total_price)
            quantity += 1
            new_product_data = {
                "product": product_id,
                "name": name,
                "price": price_id,
                "quantity": quantity,
                "total_price": total_price
            }
            response = JsonResponse({'message': _('Product added to cart successfully.')})
            response.set_cookie(cookie_key, json.dumps(new_product_data), max_age=604800)
            return response

    def add_cookie_product_to_cart_get_or_create(self, product_id, quantity, total_price, cookie_key,
                                                 cookies_to_delete):
        """
        Creates or updates an entry in the database for a product added to the cart based on data
        from cookies. Handles scenarios where the product already exists or needs to be created.
        """

        product = forms.Product.objects.get(pk=product_id)  # noqa
        product_discount = self.calculate_product_discount(self.product_instance, self.latest_discount)  # noqa
        cart, created = forms.OrderItem.objects.get_or_create(
            user=self.request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        cart.quantity += 1
        cart.total_price += product_discount if product_discount else self.product_instance.price
        if not created:
            cart.quantity += quantity
            cart.total_price += total_price
            cart.save()
            response = JsonResponse({'message': _('Product added to cart successfully.')})
            cookies_to_delete.append(cookie_key)
            return response
        else:
            cart.save()
            response = JsonResponse({'message': _('Product added to cart successfully.')})
            cookies_to_delete.append(cookie_key)
            return response

    def calculate_product_discount(self, product_instance, latest_discount):  # noqa
        """
        Calculates the discount applicable to a product based on the latest discount available.
         Considers both numerical and percentage discounts, applying the one that results in the
         lower price.
        """

        try:
            if latest_discount is None:
                return None
            if product_instance.price:
                product_price = product_instance.price
            else:
                product_price = product_instance
        except AttributeError:
            if isinstance(product_instance, (int, float)):
                product_price = product_instance
            else:
                return None

        numerical_discount = latest_discount.numerical_discount
        percentage_discount = latest_discount.percentage_discount

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

    def calculate_total_price(self, product_discount, total_price):  # noqa
        """
        Calculates the total price of a product in the cart after applying any applicable discount.
        """

        if product_discount is not None:
            total_price += product_discount
        return total_price

    def prepare_response_after_adding_products(self, cookies_to_delete):  # noqa
        """
        Prepares a JSON response after adding products to the cart. Deletes the cookies that were
        processed from the response to ensure they are removed from the client's browser.
        """

        response = JsonResponse({'message': _('Product added to cart successfully.')})
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)
        return response
