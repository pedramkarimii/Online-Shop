from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.product.form_data import forms
from apps.product.permission.template_permission_seller_or_admin import CRUD


class BrandCreateView(CRUD.SellerOrAdminCreatePermissionRequiredMixinView):
    """
    Create a new brand.
    """
    permission_required = 'product.add_brand'  # noqa/

    def setup(self, request, *args, **kwargs):
        """
        Handle the GET and POST requests for creating a new brand.
        """
        self.form_class = forms.BrandCreateForm  # noqa
        self.next_page_brand_create = reverse_lazy('brand_create')  # noqa
        self.template_brand_create = 'product/brand/brand_create.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        function to handle GET request for creating a new brand.
        """
        return render(request, self.template_brand_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        """
        function to handle POST request for creating a new brand.
        """
        form = self.form_class(self.request_post, self.request_files)  # noqa
        if form.is_valid():  # noqa
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            messages.success(request, _(f'Brand created successfully {brand.name}.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating brand.'), extra_tags='error')


class AdminOrSellerBrandListView(CRUD.SellerOrAdminOrSupervisorDetailPermissionRequiredMixinView, generic.ListView):
    """
    List all brands for admin or seller.
    """
    model = forms.Brand  # noqa

    def setup(self, request, *args, **kwargs):
        """
        Handle the GET and POST requests for listing brands.
        """
        self.context_object_name = 'brand'
        self.template_name = 'user/detail/admin_or_seller/admin_or_seller_brand.html'
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        function to add extra context data to the template.
        """
        context = super().get_context_data(**kwargs) # noqa
        brands = forms.Brand.objects.all()
        get_brand = brands.filter(user=self.request.user)
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['brands'] = brands
            return context
        if not self.request.user.is_superuser:
            context['get_brand'] = get_brand
            return context
        return context


class BrandDetailView(CRUD.SellerOrAdminOrSupervisorDetailPermissionRequiredMixinView, generic.DetailView):
    """
    Detail view for a brand.
    """
    model = forms.Brand

    def setup(self, request, *args, **kwargs):
        """
        Handle the GET and POST requests for displaying a brand detail.
        """
        self.context_object_name = 'brand'
        self.template_name = 'product/brand/brand.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Return the brand instance based on the URL kwargs.
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
        function to add extra context data to the template.
        """
        context = super().get_context_data(**kwargs)
        brands = forms.Brand.objects.all()
        get_brand = brands.filter(user=self.request.user)
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['brands'] = brands
            return context
        if not self.request.user.is_superuser:
            context['get_brand'] = get_brand
            return context
        return context


class BrandUpdateView(CRUD.SellerOrAdminBrandUpdateOrDeletePermissionRequiredMixinView):
    """
    View for updating a brand.
    """
    def setup(self, request, *args, **kwargs):
        """Initialize the success_url and retrieve the brand instance."""
        self.form_class = forms.BrandUpdateForm  # noqa
        self.template_brand_update = 'product/brand/brand_update.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        function to handle GET request for updating a brand.
        """
        form = self.form_class(instance=self.brand_instance)
        return render(request, self.template_brand_update, {'form': form, 'brand': self.brand_instance})

    def post(self, request, *args, **kwargs):
        """
        function to handle POST request for updating a brand.
        """
        form = self.form_class(self.request_post, self.request_files, instance=self.brand_instance)  # noqa
        if form.is_valid():  # noqa
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            messages.success(request, _(f'Brand updated successfully: {brand.name}.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating brand.'), extra_tags='error')


class BrandDeleteView(CRUD.SellerOrAdminBrandUpdateOrDeletePermissionRequiredMixinView,
                      generic.DetailView):
    """
    View for displaying brand details and providing an option for soft deletion.
    """
    model = forms.Brand
    template_name = 'product/brand/brand_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display brand details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'brand': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the brand.
        """
        brand = self.get_object()
        forms.Brand.soft_delete.filter(pk=brand.id).delete()
        messages.success(request, _(f'Brand has been successfully soft deleted {brand.name}.'), extra_tags='success')
        return redirect('home')
