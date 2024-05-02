from django.contrib.auth import views
from apps.account.form_data import forms
from django.urls import reverse_lazy
from apps.core.mixin.mixin_views_template import HttpsOptionLoginMixin as MustBeLogoutCustomView


class UserPasswordResetView(views.PasswordResetView, MustBeLogoutCustomView):
    """
   View for handling user password reset.
   Inherits from Django's built-in PasswordResetView.
   Attributes:
       template_name (str): The name of the template to be rendered.
       success_url (str): The URL to redirect to upon successful password reset.
       form_class (class): The form class to be used for password reset.
       http_method_names (list): List of HTTP methods allowed for this view.
       email_template_name (str): The name of the email template to be used for password reset email.
   """
    template_name = 'user/email/email_reset.html'
    success_url = reverse_lazy('resat_done')
    form_class = forms.UserPasswordResetForm
    http_method_names = ['get', 'post']
    email_template_name = 'account/email/email_reset_password.html'


class UserPasswordResetDoneView(views.PasswordResetDoneView, MustBeLogoutCustomView):
    """
    View for displaying password reset done confirmation.
    Inherits from Django's built-in PasswordResetDoneView.
    Attributes:
        template_name (str): The name of the template to be rendered.
        http_method_names (list): List of HTTP methods allowed for this view.
    """
    template_name = 'user/email/email_reset_done.html'
    http_method_names = ['get']


class UserPasswordResetConfirmView(views.PasswordResetConfirmView, MustBeLogoutCustomView):
    """
    category
    View for handling user password reset confirmation.
    Inherits from Django's built-in PasswordResetConfirmView.
    Attributes:
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to upon successful password reset.
        http_method_names (list): List of HTTP methods allowed for this view.
    """
    template_name = 'user/email/email_reset_confirm.html'
    success_url = reverse_lazy('resat_complete')
    http_method_names = ['get', 'post']


class UserPasswordResetCompleteView(views.PasswordResetCompleteView, MustBeLogoutCustomView):
    """
    View for displaying password reset completion.
    Inherits from Django's built-in PasswordResetCompleteView.
    Attributes:
        template_name (str): The name of the template to be rendered.
        http_method_names (list): List of HTTP methods allowed for this view.
    """
    template_name = 'user/email/email_reset_complete.html'
    http_method_names = ['get']
