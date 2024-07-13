from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views, login, logout
from django.utils.translation import gettext_lazy as _
from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.account.models import User, UserAuth
from apps.account.users_auth.services import update_user_auth_uuid
from apps.core.mixin.mixin_views_template import HttpsOptionLoginMixin as MustBeLogoutCustomView, \
    HttpsOptionNotLogoutMixin as MustBeLogingCustomView
from apps.core.otp_sms import CodeGenerator


class SuccessLoginView(MustBeLogoutCustomView, views.LoginView):
    """
    Handles user login.
    Inherits from CustomView and LoginView classes.
    """
    http_method_names = ['get', 'post']
    next_page = reverse_lazy('home')

    def setup(self, request, *args, **kwargs):
        """Initialize the next_page_create_profile, get profile."""
        self.next_page_create_profile = reverse_lazy('create_profile')  # noqa
        self.get_profile = hasattr(request.user, 'profile')  # noqa
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Process the form submission after successful validation.
        If the user has a profile with age and name, display a success message.
        If the profile is incomplete, redirect to complete it.
        """
        response = super().form_valid(form)
        if self.get_profile and self.request.user.profile.age and self.request.user.profile.name:
            messages.success(self.request, _('You have logged in successfully.'), extra_tags='success')
        else:
            messages.warning(self.request,
                             _('Please complete your profile.'), extra_tags='warning')
            return redirect(self.next_page_create_profile)
        return response


class UserLogoutView(MustBeLogingCustomView):
    """
    Handles user logout.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.next_page_home = reverse_lazy('home')  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for logging out.
        Logs out the user, clears session, and redirects to the home page with a success message.
        """
        if request.user.is_authenticated:
            logout(self.request)
            messages.success(request, _('Logout successfully'), extra_tags='success')
            request.session.flush()
            return redirect(self.next_page_home)


class UserLoginPhoneNumberView(MustBeLogoutCustomView):
    """
    View for user login phone number.
    Renders login form and handles form submission for user login.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form, next_page_login_verify_code, next_page_login, next_page_home,
         template_name, template name."""
        self.form = forms.UserPhoneNumberLoginForm  # noqa
        self.next_page_login_verify_code = reverse_lazy('login_verify_code')  # noqa
        self.next_page_login = reverse_lazy('login')  # noqa
        self.template_login = 'public/home/login/login_phone_number.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
         Handle GET requests to display the login form.
         Renders the login form with an instance of the UserLoginForm.
         """
        return render(request, self.template_login, {'form': self.form()})

    def post(self, request):
        """
        Handle POST requests to process the login form submission.
        If form is valid, store user login information in session and send an OTP code.
        If the user exists, generate and send OTP code, then redirect to verify code page.
        If form is not valid, display error messages and redirect back to login page.
        """
        form = self.form(request.POST)
        if form.is_valid():
            request.session['user_login_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
            }
            phone_number = form.cleaned_data['phone_number']
            user_exists = forms.User.objects.filter(phone_number=phone_number).exists()
            if user_exists:
                code_generator = CodeGenerator()
                code_generator.generate_and_store_code(phone_number)
                messages.success(request, _('Code sent to your phone number'), extra_tags='success')
                return redirect(self.next_page_login_verify_code)
            else:
                messages.error(request, _('Phone number or password is not valid'), extra_tags='error')
                return redirect(self.next_page_login)
        return render(request, self.template_login, {'form': form})


class UserLoginUsernameOrEmailView(MustBeLogoutCustomView):
    """
    Custom view for user login via username or email.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form, next_page_login_verify_code, next_page_login, next_page_home,
         template_name, template name."""
        self.form = forms.UserLoginUsernameOrEmailForm  # noqa
        self.next_page_login = reverse_lazy('login')  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_login = 'public/home/login/login.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        for GET requests, render the login form with an instance of the UserLoginUsernameOrEmailForm.
        """
        return render(request, self.template_login, {'form': self.form()})

    def post(self, request):
        """
        for POST requests, process the login form submission.
        If the form is valid, check if the user exists with the provided username or email.
        If the user exists, log them in, generate and store access and refresh tokens, and redirect to the home page.
        If the user does not exist, display an error message and redirect back to the login page.
        """
        form = self.form(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['username_or_email']  # noqa
            if '@' in email_or_username:
                try:
                    user = User.objects.get(email=email_or_username)
                except User.DoesNotExist:
                    user = None
            else:
                try:
                    user = User.objects.get(username=email_or_username)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user, backend='apps.account.users_auth.authenticate.EmailAuthBackend')
                update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.ACCESS_TOKEN)
                update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.REFRESH_TOKEN)
                messages.success(request, _('Login successful'), extra_tags='success')
                return redirect(self.next_page_home)
            else:
                messages.error(request, _('Username or Email or Password is not valid'), extra_tags='error')
                return redirect(self.next_page_login)


class UserLoginEmailView(MustBeLogoutCustomView):
    """
    Defines a view for user login via email.
    Handles GET and POST requests.
    Sets up necessary attributes such as form_class, URLs, and templates.
    Includes a method to send OTP email and create OptCode instance.
    Handles form submission and OTP email sending logic.
    Displays appropriate messages based on email verification status.
    """

    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form_class, next_page_login_verify_code_email, template_login_email.
        """
        self.form_class = forms.UserLoginEmailForm  # noqa
        self.next_page_login_verify_code_email = reverse_lazy('login_verify_code_email')  # noqa
        self.next_page_login_email = reverse_lazy('login_email')  # noqa
        self.template_login_email = 'public/home/login/login_email.html'  # noqa
        self.code_generator = CodeGenerator()  # noqa
        return super().setup(request, *args, **kwargs)

    def send_otp_email(self, email, otp):
        """
        Sends an OTP code to the provided email address.
        """
        user = forms.User.objects.get(email=email)
        if user:
            subject = 'Your OTP for Verification'
            message = f'Your OTP for login is (Expiry date two minutes): {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(self.request, _('Code sent to your Email'), extra_tags='success')
        elif not user:
            messages.error(self.request, _('Invalid email or password'), extra_tags='error')
            return redirect(self.next_page_login_email)
        else:
            messages.success(self.request, _('Invalid email or password'), extra_tags='error')
            return redirect(self.next_page_login_email)

    def get(self, request):
        """
        Handles GET requests to display the login email form.
        """
        return render(request, self.template_login_email, {'form': self.form_class()})

    def post(self, request):
        """
        Handles POST requests to process the login email form submission.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = self.code_generator.generate_and_store_code(email)
            if otp and email:
                stored_code = otp.decode('utf-8') if isinstance(otp, bytes) else otp
                self.send_otp_email(email, stored_code)
                request.session['user_login_info'] = {'email': email}
                return redirect(self.next_page_login_verify_code_email)
            else:
                messages.error(request, _('Invalid email or password'), extra_tags='error')
                return redirect(self.next_page_login_email)

        return render(request, self.template_login_email, {'form': form})
