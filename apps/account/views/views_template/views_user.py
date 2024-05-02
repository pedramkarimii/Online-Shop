from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from apps.account.form_data import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from apps.account.models import User
from apps.core.mixin.mixin_views_template import HttpsOptionNotLogoutMixin as MustBeLogingCustomView


class UserUpdateView(MustBeLogingCustomView):
    """
    View for changing user information.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form_class, next_page_home, next_page_change_user, user_instance, template name.
        Set up method to retrieve the current user instance.
        """
        self.form_class = forms.UserUpdateForm  # noqa
        self.user_instance = get_object_or_404(User, pk=kwargs['pk'])
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_change_user = reverse_lazy('change_user')  # noqa
        self.template_change_user = 'user/account/change_info_user.html'  # noqa
        self.user_instance = request.user  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display the user change form.
        Renders the user change form with the current user's information.
        """
        form = self.form_class(instance=self.user_instance)
        return render(request, self.template_change_user, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to process form submission for changing user information.
        If form is valid, save changes and display success message.
        If form is not valid, render form again with error messages.
        """
        form = self.form_class(request.POST, instance=self.user_instance)
        if form.is_valid():
            form.save()
            messages.success(request, _('User information updated successfully'), extra_tags='success')
            return redirect(self.next_page_home)
        return render(request, self.template_change_user, {'form': form})


class ChangePasswordView(MustBeLogingCustomView):
    """A view to manage password change for users."""
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form_class, next page1, page2, template name.
        """
        self.form_class = forms.ChangePasswordForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_change_pass = reverse_lazy('change_pass')  # noqa
        self.template_change_password = 'user/account/change_password.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """Render the change password form."""
        form = self.form_class(request.user)
        return render(request, self.template_change_password, {'form': form})

    def post(self, request):
        """Handle password change form submission."""
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'), extra_tags='success')
            return redirect(self.next_page_home)
        return render(request, self.template_change_password, {'form': form})


class UserDeleteView(DetailView, MustBeLogingCustomView):
    """
    View for displaying user details and providing an option for soft deletion.
    """
    model = User
    template_name = 'user/account/user_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display user details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'user': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the user.
        """
        user = self.get_object()
        User.soft_delete.filter(pk=user.id).delete()
        messages.success(request, _(f'User has been successfully soft deleted {User.username}.'), extra_tags='success')
        return redirect('home')
