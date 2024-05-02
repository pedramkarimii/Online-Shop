from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.product.form_data import forms
from apps.product.models import Media
from apps.product.permission.template_permission_seller_or_admin import CRUD


class ProductCreateView(CRUD.SellerOrAdminCreatePermissionRequiredMixinView):

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.ProductCreateForm  # noqa
        self.next_page_product_create = reverse_lazy('product_create')  # noqa
        self.template_product_create = 'product/product/product_create.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_product_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post, self.request_files)
        if form.is_valid():  # noqa
            product = form.save(commit=False)
            if 'product_picture' in self.request_files:
                product.save()
                images = self.request_files.getlist('product_picture')
                for image in images:
                    Media.objects.create(product=product, product_picture=image)
                messages.success(request, _(f'Product created successfully {product.name}.'), extra_tags='success')
                return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating product.'), extra_tags='error')
            return render(request, self.template_product_create, {'form': form})


class AdminOrSellerProductListView(CRUD.SellerOrAdminOrSupervisorDetailPermissionRequiredMixinView, generic.ListView):
    model = forms.Product  # noqa

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'product'
        self.template_name = 'user/detail/admin_or_seller/admin_or_seller_product.html'
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        products = forms.Product.objects.all()
        get_product = forms.Product.objects.filter(brand__user=self.request.user)

        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(  # noqa
                name='Supervisor').exists():
            context['products'] = products
            return context
        if not self.request.user.is_superuser:
            context['get_product'] = get_product
            return context
        return context


class ProductDetailView(generic.DetailView):
    http_method_names = ['get']  # noqa
    model = forms.Product

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'profile'
        self.template_name = 'product/product/product.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Return the product instance based on the URL kwargs."""
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
        context = super().get_context_data(**kwargs)
        products = self.object

        product_price = products.price

        latest_discount = products.product_code_discounts.filter(is_expired=False).order_by('-create_time').first()

        numerical_discount = None
        percentage_discount = None
        product_discount = None

        if latest_discount:  # noqa
            numerical_discount = latest_discount.numerical_discount
            percentage_discount = latest_discount.percentage_discount
        if numerical_discount and percentage_discount:  # noqa
            product_numerical_discount = product_price - numerical_discount
            product_percentage_discount = product_price - (product_price * percentage_discount / 100)
            if product_numerical_discount < product_percentage_discount:
                product_discount = product_numerical_discount
                numerical_discount = None  # noqa
                percentage_discount = None  # noqa
        if numerical_discount is not None:
            product_discount = product_price - numerical_discount
        if percentage_discount is not None:
            product_discount = product_price - (product_price * percentage_discount / 100)

        if not product_discount and not numerical_discount:
            product_discount = None

        context['product'] = products
        context['discount'] = product_discount
        return context


class ProductUpdateView(CRUD.SellerOrAdminProductUpdateOrDeletePermissionRequiredMixinView):

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url and retrieve the product instance."""
        self.product_instance = get_object_or_404(forms.Product, pk=kwargs['pk'])  # noqa
        self.form_class = forms.ProductUpdateForm  # noqa
        self.template_product_update = 'product/product/product_update.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.product_instance)
        return render(request, self.template_product_update, {'form': form, 'product': self.product_instance})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post, self.request_files, instance=self.product_instance)  # noqa
        if form.is_valid():  # noqa
            product = form.save(commit=False)
            if 'product_picture' in self.request_files:
                product.save()
                images = self.request_files.getlist('product_picture')
                for image in images:
                    Media.objects.create(product=product, product_picture=image)
                messages.success(request, _(f'Product updated successfully {product.name}.'), extra_tags='success')
                return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating product.'), extra_tags='error')
            return render(request, self.template_product_update, {'form': form})


class ProductDeleteView(CRUD.SellerOrAdminProductUpdateOrDeletePermissionRequiredMixinView,
                        generic.DetailView):
    """
    View for displaying product details and providing an option for soft deletion.
    """
    model = forms.Product
    template_name = 'product/product/product_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display product details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'product': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the product.
        """
        product = self.get_object()
        forms.Product.soft_delete.filter(pk=product.id).delete()
        messages.success(request, _(f'Product has been successfully soft deleted {product.name}.'),
                         extra_tags='success')
        return redirect('home')
