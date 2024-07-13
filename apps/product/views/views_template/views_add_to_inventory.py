from django.views import generic
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.product.form_data import forms
from apps.core.permission.template_permission_admin import CRUD


class AddToInventoryCreateView(CRUD.AdminPermissionRequiredMixinView):
    """
    View for creating a new warehouse keeper entry.
    Inherits from CRUD.AdminPermissionRequiredMixinView for admin permission checks.
    Attributes:
    form_class (forms.AddToInventoryCreateForm): Form class for creating a new inventory entry.
    next_page_warehouse_keeper_create (str): URL to redirect after successful creation.
    template_add_to_inventory_create (str): Template to render for the create view.
    request_post (dict): POST data received in the request.
    """

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.form_class = forms.AddToInventoryCreateForm  # noqa
        self.next_page_warehouse_keeper_create = reverse_lazy('warehouse_keeper_create')  # noqa
        self.template_add_to_inventory_create = 'product/warehouse_keeper/warehouse_keeper_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to the view. Renders the form for creating a new warehouse keeper entry.
        """
        return render(request, self.template_add_to_inventory_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        """
        function to handle post request on the view. Creates a new warehouse keeper entry if the form is valid.
        """
        form = self.form_class(self.request_post)
        if form.is_valid():  # noqa
            warehouse_keeper = form.save(commit=False)
            warehouse_keeper.save()
            messages.success(request, _(f'Warehouse Keeper created successfully.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating warehouse keeper.'), extra_tags='error')


class AdminAddToInventoryListView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    """
    class to handle the list view for warehouse keeper entries
    """
    http_method_names = ['get']  # noqa
    model = forms.AddToInventory

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'warehouse_keeper'
        self.template_name = 'user/detail/admin/admin_warehouse_keeper.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        """
        function to get the queryset for the view.
        """
        return forms.AddToInventory.objects.all()

    def get_context_data(self, **kwargs):
        """
        function to get the context data for the view.
        """
        context = super().get_context_data(**kwargs)  # noqa
        warehouse_keepers = forms.AddToInventory.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_warehouse_keeper'] = warehouse_keepers
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_warehouse_keeper'] = warehouse_keepers
            return context


class AddToInventoryDetailView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    """
    class to handle the detail view for warehouse keeper entries
    """
    http_method_names = ['get']  # noqa
    model = forms.AddToInventory

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'warehouse_keeper'
        self.template_name = 'product/warehouse_keeper/warehouse_keeper.html'
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
        warehouse_keeper = forms.AddToInventory.objects.all()
        context['warehouse_keeper'] = warehouse_keeper
        return context


class AddToInventoryUpdateView(CRUD.AdminPermissionRequiredMixinView):
    """
    class to handle the update view for warehouse keeper entries
    """
    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.form_class = forms.AddToInventoryUpdateForm  # noqa
        self.template_warehouse_keeper_update = 'product/warehouse_keeper/warehouse_keeper_update.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        function to handle get request on the view. Renders the form for updating a warehouse keeper entry.
        """
        form = self.form_class(instance=self.add_to_inventory_instance_instance)
        return render(request, self.template_warehouse_keeper_update,
                      {'form': form, 'warehouse_keeper': self.add_to_inventory_instance_instance})

    def post(self, request, *args, **kwargs):
        """
        function to handle post request on the view. Updates a warehouse keeper entry if the form is valid.
        """
        form = self.form_class(self.request_post, instance=self.add_to_inventory_instance_instance)  # noqa
        if form.is_valid():  # noqa
            add_to_inventory = form.save(commit=False)
            add_to_inventory.user = add_to_inventory.inventory.user
            add_to_inventory.save()
            messages.success(request, _(f'Warehouse Keeper updated successfully.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating warehouse keeper.'), extra_tags='error')


class AddToInventoryDeleteView(CRUD.AdminPermissionRequiredMixinView, DetailView):
    """
    class to handle the delete view for warehouse keeper entries
    """
    model = forms.AddToInventory
    template_name = 'product/warehouse_keeper/warehouse_keeper_delete.html'

    def get(self, request, *args, **kwargs):
        """
        function to handle get request on the view. Renders the confirmation page for deleting a warehouse keeper entry.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'warehouse_keeper': self.object})

    def post(self, request, *args, **kwargs):
        """
        function to handle post request on the view. Soft deletes a warehouse keeper entry.
        """
        add_to_inventory = self.get_object()
        forms.AddToInventory.soft_delete.filter(pk=add_to_inventory.id).delete()
        messages.success(request, _(f'Warehouse Keeper has been successfully soft deleted.'), extra_tags='success')
        return redirect(self.next_page_home)
