from django.views import generic  # noqa
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.product.form_data import forms
from apps.core.permission.template_permission_admin import CRUD


class InventoryCreateView(CRUD.AdminPermissionRequiredMixinView):
    """
    Create a new inventory.
    """
    def setup(self, request, *args, **kwargs):
        """
        Handle the GET and POST requests for creating a new inventory.
        """
        self.form_class = forms.InventoryCreateForm  # noqa
        self.next_page_inventory_create = reverse_lazy('inventory_create')  # noqa
        self.template_inventory_create = 'product/inventory/inventory_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Render the form for creating a new inventory.
        """
        return render(request, self.template_inventory_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request for creating a new inventory.
        """
        form = self.form_class(self.request_post)  # noqa
        if form.is_valid():  # noqa
            inventory = form.save(commit=False)
            inventory.save()
            messages.success(request, _(f'Inventory created successfully.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating Inventory.'), extra_tags='error')


class AdminInventoryListView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    """
    class to handle the list view for warehouse keeper entries
    """
    http_method_names = ['get']  # noqa
    model = forms.Inventory

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'inventory'
        self.template_name = 'user/detail/admin/admin_inventory.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        """
        function to get the queryset for the view.
        """
        return forms.Inventory.objects.all()

    def get_context_data(self, **kwargs):
        """
        function to get the context data for the view.
        """
        context = super().get_context_data(**kwargs)  # noqa
        inventory = forms.Inventory.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_inventories'] = inventory
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_inventories'] = inventory
            return context


class InventoryDetailView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    """
    Detail view for a warehouse keeper.
    """
    http_method_names = ['get']  # noqa
    model = forms.Inventory

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'inventory'
        self.template_name = 'product/inventory/inventory.html'
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
        inventory = forms.Inventory.objects.all()
        context['inventory'] = inventory
        return context


class InventoryUpdateView(CRUD.AdminPermissionRequiredMixinView):

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url and retrieve the warehouse keeper instance."""

        self.form_class = forms.InventoryUpdateForm  # noqa
        self.template_inventory_update = 'product/inventory/inventory_update.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.inventory_instance)
        return render(request, self.template_inventory_update,
                      {'form': form, 'inventory': self.inventory_instance})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post, instance=self.inventory_instance)  # noqa
        if form.is_valid():  # noqa
            inventory = form.save(commit=False)
            inventory.save()
            messages.success(request, _(f'Inventory updated successfully.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating Inventory.'), extra_tags='error')


class InventoryDeleteView(CRUD.AdminPermissionRequiredMixinView, DetailView):
    """
    View for displaying warehouse keeper details and providing an option for soft deletion.
    """
    model = forms.Inventory
    template_name = 'product/inventory/inventory_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display inventory details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'inventory': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the inventory.
        """
        inventory = self.get_object()
        forms.Inventory.soft_delete.filter(pk=inventory.id).delete()
        messages.success(request, _(f'Inventory has been successfully soft deleted.'), extra_tags='success')
        return redirect(self.next_page_home)
