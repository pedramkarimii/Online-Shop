from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.account.form_data import forms
from django.shortcuts import render, redirect, get_object_or_404
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
