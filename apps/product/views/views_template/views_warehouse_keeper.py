from django.views import generic
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.product.form_data import forms
from apps.core.permission.template_permission_admin import CRUD


class WarehouseKeeperCreateView(CRUD.AdminPermissionRequiredMixinView):
    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.WarehouseKeeperCreateForm  # noqa
        self.next_page_warehouse_keeper_create = reverse_lazy('warehouse_keeper_create')  # noqa
        self.template_warehouse_keeper_create = 'product/warehouse_keeper/warehouse_keeper_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_warehouse_keeper_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post)
        if form.is_valid():  # noqa
            warehouse_keeper = form.save(commit=False)
            warehouse_keeper.user = warehouse_keeper.brand.user
            warehouse_keeper.save()
            messages.success(request, _(f'Warehouse Keeper created successfully.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating warehouse keeper.'), extra_tags='error')


class AdminWarehouseKeeperListView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    http_method_names = ['get']  # noqa
    model = forms.WarehouseKeeper

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'warehouse_keeper'
        self.template_name = 'user/detail/admin/admin_warehouse_keeper.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return forms.WarehouseKeeper.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        warehouse_keepers = forms.WarehouseKeeper.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_warehouse_keeper'] = warehouse_keepers
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_warehouse_keeper'] = warehouse_keepers
            return context


class WarehouseKeeperDetailView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    http_method_names = ['get']  # noqa
    model = forms.WarehouseKeeper

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'warehouse_keeper'
        self.template_name = 'product/warehouse_keeper/warehouse_keeper.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Return the warehouse keeper instance based on the URL kwargs."""  # noqa
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
        warehouse_keeper = forms.WarehouseKeeper.objects.all()
        context['warehouse_keeper'] = warehouse_keeper
        return context


class WarehouseKeeperUpdateView(CRUD.AdminPermissionRequiredMixinView):

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url and retrieve the warehouse keeper instance."""

        self.form_class = forms.WarehouseKeeperUpdateForm  # noqa
        self.template_warehouse_keeper_update = 'product/warehouse_keeper/warehouse_keeper_update.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.warehouse_keeper_instance)
        return render(request, self.template_warehouse_keeper_update,
                      {'form': form, 'warehouse_keeper': self.warehouse_keeper_instance})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post, instance=self.warehouse_keeper_instance)  # noqa
        if form.is_valid():  # noqa
            warehouse_keeper = form.save(commit=False)
            warehouse_keeper.user = warehouse_keeper.brand.user
            warehouse_keeper.save()
            messages.success(request, _(f'Warehouse Keeper updated successfully.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating warehouse keeper.'), extra_tags='error')


class WarehouseKeeperDeleteView(CRUD.AdminPermissionRequiredMixinView, DetailView):
    """
    View for displaying warehouse keeper details and providing an option for soft deletion.
    """
    model = forms.WarehouseKeeper
    template_name = 'product/warehouse_keeper/warehouse_keeper_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display warehouse keeper details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'warehouse_keeper': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the warehouse keeper.
        """
        warehouse_keeper = self.get_object()
        forms.WarehouseKeeper.soft_delete.filter(pk=warehouse_keeper.id).delete()
        messages.success(request, _(f'Warehouse Keeper has been successfully soft deleted.'), extra_tags='success')
        return redirect('home')
