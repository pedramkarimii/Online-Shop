from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.core.permission.template_permission_admin import CRUD


class RoleCreateView(CRUD.AdminPermissionRequiredMixinView):

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.RoleCreateForm  # noqa
        self.next_page_product_create = reverse_lazy('role_create')  # noqa
        self.template_role_create = 'user/role/role_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_role_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post)
        if form.is_valid():
            print(form.cleaned_data)
            roles = form.save(commit=False)
            roles.save()
            messages.success(request, _(f'Role created successfully .'),
                             extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating Role .'), extra_tags='error')
            return render(request, self.template_role_create, {'form': form})


class AdminRoleListView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    http_method_names = ['get']  # noqa
    model = forms.Role

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'role'
        self.template_name = 'user/detail/admin/admin_role.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return forms.Role.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        roles = forms.Role.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_role'] = roles
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_role'] = roles
            return context


class RoleDetailView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    http_method_names = ['get']  # noqa
    model = forms.Role

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'role'
        self.template_name = 'user/role/role.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Return the role instance based on the URL kwargs."""  # noqa
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
        role = forms.Role.objects.all()
        context['role'] = role
        return context


class RoleUpdateView(CRUD.AdminPermissionRequiredMixinView):

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.RoleUpdateForm  # noqa
        self.next_page_product_create = reverse_lazy('role_update')  # noqa
        self.template_role_update = 'user/role/role_update.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.role_instance)
        return render(request, self.template_role_update, {'form': form, 'role': self.role_instance})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post, instance=self.role_instance)
        if form.is_valid():
            print(form.cleaned_data)
            roles = form.save(commit=False)
            roles.save()
            messages.success(request, _(f'Role updated successfully .'),
                             extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating Role .'), extra_tags='error')
            return render(request, self.template_role_update, {'form': form, 'role': self.role_instance})


class RoleDeleteView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    model = forms.Role
    template_name = 'user/role/role_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display warehouse keeper details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'role': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the warehouse keeper.
        """
        role = self.get_object()
        forms.Role.soft_delete.filter(pk=role.id).delete()
        messages.success(request, _(f'Role has been successfully soft deleted.'), extra_tags='success')
        return redirect(self.next_page_home)
