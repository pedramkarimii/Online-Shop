from datetime import datetime
import redis
import pytz
from django.contrib import messages
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from apps.account.models import User, UserAuth
from apps.account.users_auth.services import update_user_auth_uuid
from apps.core.mixin.mixin_views_template import HttpsOptionLoginMixin as MustBeLogoutCustomView
from apps.core.otp_sms import CodeGenerator


class LoginVerifyCodeView(MustBeLogoutCustomView):
    """
    View for verifying login code.

    Renders the code verification form and handles form submission.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form, next_page_login_verify_code, next_page_success_login,
        next_page_login, next_page_home, template name."""
        self.form = forms.VerifyCodeForm  # noqa
        self.next_page_login_verify_code = reverse_lazy('login_verify_code')  # noqa
        self.next_page_success_login = reverse_lazy('success_login')  # noqa
        self.next_page_login = reverse_lazy('login')  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_verifycode = 'public/home/login/verify_code.html'  # noqa
        self.redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        Handle GET requests to display the code verification form.

        Renders the code verification form.
        """
        return render(request, self.template_verifycode, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user_session = request.session['user_login_info']
            user = forms.User.objects.filter(phone_number=user_session['phone_number'])
            if user.exists():

                code_instance = self.redis_client.get(user_session['phone_number'])
                if not code_instance:  # noqa
                    messages.error(request, _('Code is expired'), extra_tags='error')
                try:
                    stored_code = code_instance.decode('utf-8')
                except AttributeError:
                    return redirect(self.next_page_login_verify_code)
                current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
                expiration_time = current_time + timezone.timedelta(minutes=2)
                code = request.POST.get('code')
                if (code == stored_code and expiration_time > current_time):  # noqa
                    user = user.first()  # noqa
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.ACCESS_TOKEN)
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.REFRESH_TOKEN)
                    self.redis_client.delete(code_instance)
                    messages.success(request, _('Code verified successfully'), extra_tags='success')
                    return redirect(self.next_page_success_login)
                elif expiration_time < current_time:
                    self.redis_client.delete(code_instance)
                    messages.error(request, _('Code is expired'), extra_tags='error')
                else:
                    messages.error(request, _('Code is not valid'), extra_tags='error')

            else:
                messages.error(request, _('Phone number or password is not valid'), extra_tags='error')
                return redirect(self.next_page_login)


class UserRegisterView(MustBeLogoutCustomView):
    """
    Handles user registration.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form_class, next_page_verify_code, next_page_register_user,
        next_page_home, template name."""
        self.form_class = forms.UserRegistrationForm  # noqa
        self.next_page_verify_code = reverse_lazy('verify_code')  # noqa
        self.next_page_register_user = reverse_lazy('user_create')  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_create_user = 'user/account/create_user.html'  # noqa
        self.code_generator = CodeGenerator()  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
       Handle GET requests to display the user registration form.
       Renders the user registration form.
       """
        return render(request, self.template_create_user, {'form': self.form_class()})

    def post(self, request):
        """
        Handle POST requests to process the user registration form submission.
        If form is valid, generate and send OTP code, and store registration info in session.
        If form is not valid, display error messages.
        """

        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():

            phone_number = form.cleaned_data['phone_number']
            self.code_generator.generate_and_store_code(phone_number)
            request.session['user_registration_info'] = {
                'phone_number': phone_number,
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password2'],
            }
            messages.success(request, _('Code sent to your phone number'), extra_tags='success')
            return redirect(self.next_page_verify_code)
        else:
            messages.error(request, _('Form is not valid'), extra_tags='error')
            return redirect(self.next_page_register_user)


class UserRegistrationVerifyCodeView(MustBeLogoutCustomView):
    """
    Handles verification of registration code for user registration.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form_class, next_page_home, next_page_login_verify_code, template name."""
        self.form_class = forms.VerifyCodeForm  # noqa
        self.next_page_login = reverse_lazy('login')  # noqa
        self.next_page_login_verify_code = reverse_lazy('verify_code')  # noqa
        self.next_page_user_create = reverse_lazy('user_create')  # noqa
        self.template_verifycode = 'public/home/login/verify_code.html'  # noqa
        self.redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        Handle GET requests to display the code verification form for user registration.
        Renders the code verification form.
        """
        return render(request, self.template_verifycode, {'form': self.form_class()})

    def post(self, request):
        """
        Handle POST requests to process the code verification form submission for user registration.
        Retrieves user registration information from session and verifies the entered code.
        If the code is valid and not expired, creates the user and redirects to home page.
        If the code is expired or invalid, displays error messages and redirects back to verification page.
        """
        user_session = request.session['user_registration_info']
        code_instance = self.redis_client.get(user_session['phone_number'])

        form = self.form_class(request.POST)
        if form.is_valid():
            if not code_instance:  # noqa
                messages.error(request, _('Code is expired'), extra_tags='error')
            try:
                stored_code = code_instance.decode('utf-8')
            except AttributeError:
                return redirect(self.next_page_login_verify_code)

            current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
            expiration_time = current_time + timezone.timedelta(minutes=2)
            if request.POST['code'] == stored_code and expiration_time > current_time:  # noqa
                User.objects.create_user(
                    phone_number=user_session['phone_number'],
                    email=user_session['email'],
                    username=user_session['username'],
                    password=user_session['password'],
                )
                self.redis_client.delete(code_instance)
                messages.success(request, _('User created successfully'), extra_tags='success')
                return redirect(self.next_page_login)
            elif expiration_time < current_time:
                self.redis_client.delete(code_instance)
                messages.error(request, _('Code is expired'), extra_tags='error')
                return redirect(self.next_page_login_verify_code)
        else:
            messages.error(request, _('Code is not valid'), extra_tags='error')
            return redirect(self.next_page_login_verify_code)


class LoginVerifyCodeEmailView(MustBeLogoutCustomView):
    """
    Defines a view for verifying login codes sent via email.
    Handles GET and POST requests.
    Sets up necessary attributes such as form_class, URLs, and templates.
    Handles form submission and code verification logic.
    Displays appropriate messages based on verification status.
    """

    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form_class, next_page_login_verify_code_email, template_login_email.
        """
        self.form_class = forms.VerifyCodeForm  # noqa
        self.next_page_login_email = reverse_lazy('login_email')  # noqa
        self.next_page_success_login = reverse_lazy('success_login')  # noqa
        self.next_page_login_verify_code = reverse_lazy('login_verify_code_email')  # noqa
        self.template_verifycode = 'public/home/login/verify_code.html'  # noqa
        self.redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_verifycode, {'form': self.form_class()})

    def post(self, request):

        user_session = request.session.get('user_login_info')
        user = forms.User.objects.filter(email=user_session['email'])
        form = self.form_class(request.POST)
        if form.is_valid():  # noqa
            if user.exists():

                code_instance = self.redis_client.get(user_session['email'])

                if not code_instance:  # noqa
                    messages.error(request, _('Code is expired'), extra_tags='error')
                try:
                    stored_code = code_instance.decode('utf-8')
                except AttributeError:
                    return redirect(self.next_page_login_verify_code)

                current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
                expiration_time = current_time + timezone.timedelta(minutes=2)
                if request.POST['code'] == stored_code and expiration_time > current_time:  # noqa
                    user = user.first()  # noqa
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.ACCESS_TOKEN)
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.REFRESH_TOKEN)
                    self.redis_client.delete(code_instance)
                    messages.success(request, _('Code verified successfully'), extra_tags='success')
                    return redirect(self.next_page_success_login)
                elif expiration_time < current_time:
                    messages.error(request, _('Code is expired'), extra_tags='error')
                    self.redis_client.delete(code_instance)
                    return redirect(self.next_page_login_email)
            else:
                messages.error(request, _('Code is not a valid'), extra_tags='error')
                return redirect(self.next_page_login_verify_code)
        else:
            messages.error(request, _('Code is not valid', 'error'))
            return redirect(self.next_page_login_verify_code)
