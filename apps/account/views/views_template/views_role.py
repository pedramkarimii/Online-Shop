from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic

from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.core.permission.template_permission_admin import CRUD


class RoleCreateView(CRUD.AdminPermissionRequiredMixinView):
    """
    View for creating a new role. Inherits from CRUD.AdminPermissionRequiredMixinView.
    Attributes:
    - form_class: The form class to use for role creation.
    - next_page_product_create: URL to redirect after role creation.
    - template_role_create: Template to render for role creation.
    - request_post: POST data from the request.
    Methods:
    - setup: Initializes attributes such as form_class, next_page_product_create, template_role_create, and request_post.
    - get: Handles GET request for role creation page.
    - post: Handles POST request for creating a new role.
    """

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.RoleCreateForm  # noqa
        self.next_page_product_create = reverse_lazy('role_create')  # noqa
        self.template_role_create = 'user/role/role_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET request for role creation page."""
        return render(request, self.template_role_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        """Handle POST request for creating a new role."""
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
    """
    View for listing all roles. Inherits from CRUD.AdminPermissionRequiredMixinView and generic.ListView.
    Attributes:
    - model: The model used for listing roles.
    Methods:
    - setup: Initializes attributes such as context_object_name and template_name.
    - get_queryset: Retrieves the queryset of roles to be listed.
    - get_context_data: Adds context data based on user permissions.
    """
    http_method_names = ['get']  # noqa
    model = forms.Role

    def setup(self, request, *args, **kwargs):
        """Initialize attributes for role list view."""
        self.context_object_name = 'role'
        self.template_name = 'user/detail/admin/admin_role.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        """Retrieve all roles for listing."""
        return forms.Role.objects.all()

    def get_context_data(self, **kwargs):
        """Add context data based on user permissions."""
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
    """
    View for displaying details of a role. Inherits from CRUD.AdminPermissionRequiredMixinView and generic.DetailView.
    Attributes:
    - model: The model used for role details.
    Methods:
    - setup: Initializes attributes such as context_object_name and template_name.
    - get_object: Retrieves the role object based on URL kwargs.
    - get_context_data: Adds context data for role details view.
    """
    http_method_names = ['get']  # noqa
    model = forms.Role

    def setup(self, request, *args, **kwargs):
        """Initialize attributes for role detail view."""
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
        """Add context data for role details view."""
        context = super().get_context_data(**kwargs)
        role = forms.Role.objects.all()
        context['role'] = role
        return context


class RoleUpdateView(CRUD.AdminPermissionRequiredMixinView):
    """
    View for updating a role. Inherits from CRUD.AdminPermissionRequiredMixinView.
    Attributes:
    - form_class: The form class to use for role update.
    - next_page_product_create: URL to redirect after role update.
    - template_role_update: Template to render for role update.
    - request_post: POST data from the request.
    Methods:
    - setup: Initializes attributes such as form_class, next_page_product_create, template_role_update, and request_post.
    - get: Handles GET request for role update page.
    - post: Handles POST request for updating a role.
    """

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.RoleUpdateForm  # noqa
        self.next_page_product_create = reverse_lazy('role_update')  # noqa
        self.template_role_update = 'user/role/role_update.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET request for role update page."""
        form = self.form_class(instance=self.role_instance)
        return render(request, self.template_role_update, {'form': form, 'role': self.role_instance})

    def post(self, request, *args, **kwargs):
        """Handle POST request for updating a role."""
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
    """
    View for deleting a role. Inherits from CRUD.AdminPermissionRequiredMixinView and generic.DetailView.
    Attributes:
    - model: The model used for role deletion.
    - template_name: Template to render for role deletion.
    Methods:
    - get: Handles GET request for role deletion confirmation page.
    - post: Handles POST request for soft deletion of a role.
    """
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
