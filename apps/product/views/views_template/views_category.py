from django.contrib.postgres.search import TrigramSimilarity
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic
from apps.product.form_data import forms
from apps.core.permission.template_permission_admin import CRUD


class CategoryCreateView(CRUD.AdminPermissionRequiredMixinView):
    """
    Create a new category.
    """
    def setup(self, request, *args, **kwargs):
        """
        Handle the GET and POST requests for creating a new category.
        """
        self.form_class = forms.CategoryCreateForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_category_create = reverse_lazy('category_create')  # noqa
        self.template_category_create = 'product/category/category_create.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to the view. Renders the form for creating a new category.
        """
        return render(request, self.template_category_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to the view. Validates the form data and creates a new category if the form is valid.
        """
        form = self.form_class(self.request_post, self.request_files)  # noqa
        if forms.Category.objects.filter(name=self.request_post.get('name')).exists():
            messages.error(request, _(f'Category already exists.'), extra_tags='error')
            return redirect(self.next_page_category_create)
        if form.is_valid():  # noqa
            category = form.save(commit=False)
            category.save()
            messages.success(request, _(f'Category created successfully {category.name}.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating category.'), extra_tags='error')


class AdminCategoryListView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    """
    List all categories for admin.
    """
    http_method_names = ['get']  # noqa
    model = forms.Category

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'category'
        self.template_name = 'user/detail/admin/admin_categories.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        """
        function to get the queryset for the view.
        """
        return forms.Category.objects.all()

    def get_context_data(self, **kwargs):
        """
        function to get the context data for the view.
        """
        context = super().get_context_data(**kwargs)  # noqa
        categories = forms.Category.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_categories'] = categories
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_categories'] = categories
            return context


class CategoryDetailView(generic.DetailView):
    """
    Detail view for a category.
    """
    http_method_names = ['get']  # noqa
    model = forms.Category

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'category'
        self.template_name = 'product/category/categories.html'
        self.form_class_search = forms.SearchForm  # noqa
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        function to get the object for the view.
        """
        queryset = self.get_queryset()  # noqa
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return render(self.request, 'http_method/http_404.html')
        return obj

    def get_context_data(self, **kwargs):
        """
        function to get the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        category = self.object
        related_products = category.category_products.all().filter(is_deleted=False)
        products_search = category.category_products.all().filter(is_deleted=False)
        form_search = self.form_class_search(self.request.GET)

        for product in related_products:
            product_price = product.price  # noqa
            latest_discount = product.product_code_discounts.filter(is_expired=False).order_by('-create_time').first()
            numerical_discount = None  # noqa
            percentage_discount = None  # noqa
            product_discount = None

            if latest_discount:
                numerical_discount = latest_discount.numerical_discount
                percentage_discount = latest_discount.percentage_discount
                if numerical_discount and percentage_discount:  # noqa
                    product_numerical_discount = product_price - numerical_discount
                    product_percentage_discount = product_price - (product_price * percentage_discount / 100)
                    if product_numerical_discount < product_percentage_discount:
                        product_discount = product_numerical_discount
                        numerical_discount = None
                        percentage_discount = None
                if numerical_discount is not None:
                    product_discount = product_price - numerical_discount
                if percentage_discount is not None:
                    product_discount = product_price - (product_price * percentage_discount / 100)
                if not product_discount and not numerical_discount:
                    product_discount = None

                product.discount = product_discount
                context['discount'] = product_discount
        if form_search.is_valid():
            search_query = form_search.cleaned_data.get('search')
            products_search = products_search.annotate(
                similarity=TrigramSimilarity('name', search_query) + TrigramSimilarity('description', search_query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
        context['products'] = related_products
        context['form_search'] = form_search
        context['products_search'] = products_search

        return context


class CategoryUpdateView(CRUD.AdminPermissionRequiredMixinView):
    """
    View for updating a category.
    """

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url and retrieve the category instance."""

        self.form_class = forms.CategoryUpdateForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_category_update = 'product/category/category_update.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Display the form for updating the category.
        """
        form = self.form_class(instance=self.category_instance)
        return render(request, self.template_category_update, {'form': form, 'category': self.category_instance})

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for updating the category.
        """
        form = self.form_class(self.request_post, self.request_files, instance=self.category_instance)  # noqa
        if form.is_valid():  # noqa
            category = form.save(commit=False)
            category.save()
            messages.success(request, _(f'Category updated successfully {category.name}.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating category.'), extra_tags='error')


class CategoryDeleteView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    """
    View for displaying category details and providing an option for soft deletion.
    """
    model = forms.Category
    template_name = 'product/category/category_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display category details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'category': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the category.
        """
        category = self.get_object()
        forms.Category.soft_delete.filter(pk=category.id).delete()
        messages.success(request, _(f'Category has been successfully soft deleted {category.name}.'),
                         extra_tags='success')
        return redirect('home')
