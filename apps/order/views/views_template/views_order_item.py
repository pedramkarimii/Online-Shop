import json
from django.core.signing import Signer
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic
from apps.order.form_data import forms
from apps.order import mixin
from apps.product.models import Product


class AddOrderItemView(mixin.ProductDiscountMixin):
    """
    Defines a view for adding items to a user's shopping cart, inheriting from `ProductDiscountMixin` for discount
     calculation functionality.
    """

    def add_product_to_cart_authenticated(self):  # noqa
        """
        Handles adding a product to the cart for authenticated users. It initializes a form instance using POST data.

        Checks if the form data is valid. If valid, calculates the discounted price for the product if a discount is
        available; otherwise, uses the product's regular price.

        Attempts to retrieve an existing cart item for the user and product. If not found, creates a new cart item
        with default quantity 1 and calculated total price.

        If form validation fails, returns JSON response with error details. If successful, updates cart item
        quantity and total price if item exists, or creates a new item.
        """
        form = self.form_class(self.request_post)
        if form.is_valid():
            try:
                product_discount = self.calculate_product_discount(self.product_instance,
                                                                   self.latest_discount)
                total_price = product_discount if product_discount else self.product_instance.price

                cart, created = forms.OrderItem.objects.get_or_create(
                    user=self.request.user,
                    product=self.product_instance,
                    defaults={'quantity': 1, 'total_price': total_price}
                )

                if not created:
                    cart.quantity += 1
                    cart.total_price += total_price
                    cart.save()

                response = JsonResponse({'message': _('Product added to cart successfully.')})
            except Exception as e:
                response = JsonResponse({'error': str(e)}, status=500)
        else:
            form_errors = form.errors.as_json()
            response = JsonResponse({'error': _('Invalid form data.'), 'form_errors': form.errors}, status=400)

        return response


class ShowOrderItemProductView(generic.ListView):
    """
    Defines a view for displaying items in the shopping cart, using a ListView for rendering.
    """

    def get(self, request, *args, **kwargs):  # noqa
        """
        Handles GET requests. If the user is not authenticated, calls a method to display cart items stored in cookies.
         Otherwise, displays items stored in the database.
        """
        if not request.user.is_authenticated:
            return self.show_product_order_item_cookie(request)
        else:
            return self.show_product_order_item_authenticated(request)

    def show_product_order_item_cookie(self, request):  # noqa
        """
        Fetches and displays cart items stored in cookies for non-authenticated users. Renders a template
        with cart item details and total price.
        """
        cart_items_cookies = {}
        sum_total_price = 0
        img_url = set()
        for key, value in request.COOKIES.items():
            if key.startswith('product_cart'):
                product_data = json.loads(value)
                cart_items_cookies[key] = product_data
                total_price = product_data.get('total_price', 0)
                sum_total_price += total_price
                product_id = product_data.get('product')
                product_instance = Product.objects.get(pk=product_id)
                media_instances = product_instance.media_products.all()
                for media_instance in media_instances:
                    url = media_instance.get_img()
                    img_url.add(url)
        return render(request, 'order/view_cart/order_item.html',
                      {'img_url': img_url, 'cart_items_cookies': cart_items_cookies,
                       'sum_total_price': sum_total_price})

    def show_product_order_item_authenticated(self, request):  # noqa
        """
        Fetches and displays cart items stored in the database for authenticated users. Calculates any available
         product discounts and renders a template with cart item details and total price.
        """
        cart_items = forms.OrderItem.objects.filter(user=request.user)  # noqa
        cart_data = {}
        sum_total_price = 0
        pk_product = None
        for item in cart_items:
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
                'total_price': item.total_price,
            }
        return render(request, 'order/view_cart/order_item.html',
                      {'pk_product': pk_product, 'cart_items': cart_data, 'sum_total_price': sum_total_price})


class DeleteOrderItemProductView(generic.ListView):
    """
    Defines a view for deleting items from the shopping cart, using a ListView for rendering.
    """

    def setup(self, request, *args, **kwargs):
        """
        Initializes necessary variables and retrieves the product instance based on the URL parameter `pk`.
        Uses the `Signer` to sign the product ID for secure retrieval.
        """
        self.product_instance = get_object_or_404(Product, pk=kwargs['pk'])  # noqa
        self.signer = Signer()  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.signed_product_id = self.signer.sign(str(self.product_instance.pk))  # noqa
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # noqa
        """
        Handles POST requests. If the user is not authenticated, calls a method to delete the product from the cart
         stored in cookies. Otherwise, deletes the product from the database.
        """
        if not self.user_authenticated:
            return self.delete_product_from_cart_cookie(request)
        else:
            return self.delete_product_from_cart_authenticated(request)

    def delete_product_from_cart_authenticated(self, request):
        """
        Deletes the specified product from the cart for authenticated users. Uses an atomic transaction
        to ensure database integrity and returns a JSON response indicating success or failure.
        """
        product = self.product_instance
        if self.user_authenticated:
            with transaction.atomic():
                cart_obj = forms.OrderItem.objects.filter(user=request.user, product=product).first()
                cart_obj.delete()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    def delete_product_from_cart_cookie(self, request):
        """
        Deletes the specified product from the cart stored in cookies for non-authenticated users.
        Returns a JSON response indicating success or failure and deletes the corresponding cookie.
        """
        cookie_key = f"product_cart{self.signed_product_id}"
        if cookie_key in self.request.COOKIES:
            response = JsonResponse({'success': True})
            response.delete_cookie(cookie_key)
            return response
        else:
            return JsonResponse({'success': False})


class UpdateOrderItemProductView(AddOrderItemView):
    """
    Defines a view for updating items in the shopping cart, inheriting functionality from
    `AddOrderItemView` for adding products to the cart.
    """
    def setup(self, request, *args, **kwargs):
        """
        Initializes necessary variables and retrieves the product instance based on the URL
        parameter `pk`. Uses the `Signer` to sign the product ID for secure retrieval. Also initializes form data,
         quantity, and total price for updating the cart item.
        """
        self.product_instance = get_object_or_404(Product, pk=kwargs['pk'])  # noqa
        self.signer = Signer()  # noqa
        self.user_authenticated = request.user.is_authenticated  # noqa
        self.signed_product_id = self.signer.sign(str(self.product_instance.pk))  # noqa
        self.latest_discount = self.product_instance.product_code_discounts.filter(is_expired=False,  # noqa
                                                                                   is_active=True).order_by(
            '-create_time').first()
        self.request_quantity = request.POST.get('quantity')  # noqa
        self.request_total_price = request.POST.get('total_price')  # noqa
        self.form_class = forms.OrderItemForm  # noqa
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # noqa
        """
        Handles POST requests. If the user is not authenticated, calls a method to update the
         product in the cart stored in cookies. Otherwise, updates the product in the database.
        """
        if not self.user_authenticated:
            return self.update_product_from_cart_cookie(request)
        else:
            return self.update_product_from_cart_authenticated(request)

    def update_product_from_cart_authenticated(self, request):
        """
        Updates the specified product in the cart for authenticated users. Uses an atomic
        transaction to ensure database integrity and returns a JSON response indicating success or failure.
        """
        if self.user_authenticated:
            new_quantity = int(self.request_quantity)
            new_total_price = int(self.request_total_price)
            product = self.product_instance
            with transaction.atomic():
                order_item_qs = forms.OrderItem.objects.get(user=request.user, product=product)
                order_item_qs.quantity = new_quantity
                order_item_qs.total_price = new_total_price
                order_item_qs.save()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    def update_product_from_cart_cookie(self, request):
        """
        Updates the specified product in the cart stored in cookies for non-authenticated users.
         Calculates any available product discounts, updates the cookie with the new product data,
         and returns a JSON response indicating success or failure.
        """
        new_quantity = int(self.request_quantity)
        new_total_price = int(self.request_total_price)

        product_discount = self.calculate_product_discount(self.product_instance, self.latest_discount)
        cookie_key = f"product_cart{self.signed_product_id}"
        if cookie_key in self.request.COOKIES:
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
