from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.views import View
from django.utils import timezone
from datetime import timedelta
from apps.product.form_data import forms
from django.shortcuts import render


class HomeView(View):
    """
    View for displaying home page with categories.
    """
    http_method_names = ['get']

    def setup(self, request, *args, **kwargs):
        """
        Initializes template_home, form_class_search and queryset of Category.
        """
        self.template_home = 'public/home/home.html'  # noqa
        self.form_class_search = forms.SearchForm  # noqa
        return super().setup(request, *args, **kwargs)

    def get_categories(self):  # noqa
        """
        Retrieve non-deleted categories.
        """
        return forms.Category.objects.filter(is_deleted=False, is_active=True)

    def get_products(self):  # noqa
        """
        Retrieve non-deleted products.
        """
        return forms.Product.objects.filter(is_deleted=False, is_active=True, category__is_active=True)

    def apply_discounts(self, products):  # noqa
        """
        Apply discounts to products if applicable.
        """
        for product in products:
            product_price = product.price
            latest_discount = product.product_code_discounts.filter(is_expired=False, is_active=True).order_by(
                '-create_time').first()
            numerical_discount = None
            percentage_discount = None
            if latest_discount:
                numerical_discount = latest_discount.numerical_discount
                percentage_discount = latest_discount.percentage_discount
            if numerical_discount and percentage_discount:
                product_numerical_discount = product_price - numerical_discount
                product_percentage_discount = product_price - (product_price * percentage_discount / 100)
                if product_numerical_discount < product_percentage_discount:
                    product.discount = product_numerical_discount
                else:
                    product.discount = product_percentage_discount
            elif percentage_discount:
                product.discount = product_price - (product_price * percentage_discount / 100)
            elif numerical_discount:
                product.discount = product_price - numerical_discount
            else:
                product.discount = None

    def get_products_search(self, form_search):  # noqa
        """
        Retrieve products based on search query.
        """
        products_search = forms.Product.objects.all().filter(Q(is_deleted=False), Q(is_active=True),
                                                             Q(category__is_active=True))
        search_query = form_search.cleaned_data.get('search')
        products = products_search.annotate(
            similarity=TrigramSimilarity('name', search_query) + TrigramSimilarity('description', search_query)
        ).filter(similarity__gt=0.1).order_by('-similarity')
        return products

    def get(self, request, *args, **kwargs):
        categories = self.get_categories()
        products = self.get_products()
        products_search = products
        form_search = self.form_class_search(request.GET)
        last_week = timezone.now() - timedelta(days=7)
        products_new = products.filter(create_time__gte=last_week, is_deleted=False)
        if self.apply_discounts is not None:
            self.apply_discounts(products)  # noqa
        if form_search.is_valid():
            products_search = self.get_products_search(form_search)
        admin_permissions = None
        admin_or_supervisor = None
        admin_or_seller = None
        if self.request.user.is_superuser or self.request.user.is_staff:
            admin_permissions = 'admin'
        if self.request.user.groups.filter(name='Supervisor').exists():
            admin_or_supervisor = 'supervisor'
        if self.request.user.groups.filter(name='Seller').exists():
            admin_or_seller = 'seller'
        permissions = request.user.get_all_permissions()
        return render(request, self.template_home, {
            'seller': admin_or_seller,
            'supervisor': admin_or_supervisor,
            'admin_permissions': admin_permissions,
            'permissions': permissions,
            'categories': categories,
            'products': products_search,
            'products_new': products_new,
            'form_search': form_search,
        })
