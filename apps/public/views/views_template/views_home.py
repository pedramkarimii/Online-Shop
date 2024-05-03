from django.contrib.postgres.search import TrigramSimilarity
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

    def get(self, request, *args, **kwargs):
        categories = forms.Category.objects.all().filter(is_deleted=False)
        products = forms.Product.objects.all().filter(is_deleted=False)
        products_search = forms.Product.objects.all().filter(is_deleted=False)
        form_search = self.form_class_search(request.GET)
        last_week = timezone.now() - timedelta(days=7)
        products_new = forms.Product.objects.all().filter(create_time__gte=last_week,is_deleted=False)
        numerical_discount = None
        percentage_discount = None
        product_discount = None
        for product in products:
            product_price = product.price
            latest_discount = product.product_code_discounts.filter(is_expired=False).order_by('-create_time').first()
            if latest_discount:
                numerical_discount = latest_discount.numerical_discount
                print('A' * 100, numerical_discount)
                percentage_discount = latest_discount.percentage_discount
                print('B' * 100, percentage_discount)
                if numerical_discount and percentage_discount:
                    product_numerical_discount = product_price - numerical_discount
                    print('W' * 100, product_numerical_discount)
                    product_percentage_discount = product_price - (product_price * percentage_discount / 100)
                    print('X' * 100, product_percentage_discount)
                    if product_numerical_discount < product_percentage_discount:
                        product_discount = product_numerical_discount
                        numerical_discount = None
                        percentage_discount = None
                    else:
                        product_discount = product_percentage_discount
                        numerical_discount = None
                        percentage_discount = None
                if percentage_discount:
                    product_discount = product_price - (product_price * percentage_discount / 100)

                if numerical_discount:
                    product_discount = product_price - numerical_discount

                if not product_discount and not numerical_discount:
                    product_discount = None
            product.discount = product_discount
        if form_search.is_valid():
            search_query = form_search.cleaned_data.get('search')
            products_search = products_search.annotate(
                similarity=TrigramSimilarity('name', search_query) + TrigramSimilarity('description', search_query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
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
            'discount': product_discount,
            'products_new': products_new,
            'form_search': form_search,
        })
