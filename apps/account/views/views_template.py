from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
import redis
import pytz
from django.contrib import messages
from django.contrib.auth import views, login, logout, update_session_auth_hash
from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from apps.account.models import User, UserAuth
from apps.account.users_auth.services import update_user_auth_uuid
from apps.core.mixin.mixin_views_template import HttpsOptionLoginMixin as MustBeLogoutCustomView, \
    HttpsOptionNotLogoutMixin as MustBeLogingCustomView
from utility.otp_sms import CodeGenerator

"""
Explanation of imports:
datetime: Module for working with dates and times.
send_mail: Function for sending emails.
settings: Django settings module for accessing project settings.
pytz: Module for timezone support.
messages: Module for displaying messages to users.
login, logout, update_session_auth_hash: Functions for user authentication management.
forms: Custom forms for various user-related operations.
render, redirect: Functions for rendering templates and redirecting requests.
reverse_lazy: Function for generating URLs.
timezone: Module for working with time zones.
DetailView: Generic class-based view for displaying detail pages.
Q: Object for building complex database queries.
User, UserAuth: Model classes representing users and user authentication information.
update_user_auth_uuid: Function for updating user authentication UUID.
MustBeLogoutCustomView, MustBeLoginCustomView: Custom mixins for managing login/logout status.
CodeGenerator: Function for generating OTP (One-Time Password) codes.
"""


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
            messages.success(self.request, 'You have logged in successfully.', extra_tags='success')
        else:
            messages.warning(self.request,
                             'Please complete your profile.',
                             extra_tags='warning')
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
            messages.success(request, 'Logout successfully', extra_tags='success')
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
        self.template_login = 'account/login/login_phone_number.html'  # noqa
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
                messages.success(request, 'Code sent to your phone number', extra_tags='success')
                return redirect(self.next_page_login_verify_code)
            else:
                messages.error(request, 'Phone number or password is not valid', extra_tags='error')
                return redirect(self.next_page_login)
        return render(request, self.template_login, {'form': form})


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
        self.template_verifycode = 'account/login/verify_code.html'  # noqa
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
                if not code_instance:
                    messages.error(request, 'Code not found', extra_tags='error')
                stored_code = code_instance.decode('utf-8')
                current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
                expiration_time = current_time + timezone.timedelta(minutes=2)
                code = request.POST.get('code')
                if (code == stored_code and expiration_time > current_time):  # noqa
                    user = user.first()  # noqa
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.ACCESS_TOKEN)
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.REFRESH_TOKEN)
                    self.redis_client.delete(code_instance)
                    messages.success(request, 'Code verified successfully', extra_tags='success')
                    return redirect(self.next_page_success_login)
                elif expiration_time < current_time:
                    self.redis_client.delete(code_instance)
                    messages.error(request, 'Code is expired', extra_tags='error')
                else:
                    messages.error(request, 'Code is not valid', extra_tags='error')

            else:
                messages.error(request, 'Phone number or password is not valid', extra_tags='error')
                return redirect(self.next_page_login)


class UserLoginUsernameOrEmailView(MustBeLogoutCustomView):
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form, next_page_login_verify_code, next_page_login, next_page_home,
         template_name, template name."""
        self.form = forms.UserLoginUsernameOrEmailForm  # noqa
        self.next_page_login = reverse_lazy('login')  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_login = 'account/login/login.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_login, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['username_or_email']
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
                messages.success(request, 'Login successful', extra_tags='success')
                return redirect(self.next_page_home)
            else:
                messages.error(request, 'Username or Email or Password is not valid', extra_tags='error')
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
        self.next_page_register_user = reverse_lazy('register_user')  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_create_user = 'account/create/create_user.html'  # noqa
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
        if form.is_valid():

            phone_number = form.cleaned_data['phone_number']
            self.code_generator.generate_and_store_code(phone_number)
            request.session['user_registration_info'] = {
                'phone_number': phone_number,
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password2'],
            }
            messages.success(request, 'Code sent to your phone number', extra_tags='success')
            return redirect(self.next_page_verify_code)
        else:
            messages.error(request, 'Form is not valid', extra_tags='error')
            return redirect(self.next_page_register_user)


class UserRegistrationVerifyCodeView(MustBeLogoutCustomView):
    """
    Handles verification of registration code for user registration.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """Initialize the form_class, next_page_home, next_page_login_verify_code, template name."""
        self.form_class = forms.VerifyCodeForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_login_verify_code = reverse_lazy('verify_code')  # noqa
        self.template_verifycode = 'account/login/verify_code.html'  # noqa
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
            stored_code = code_instance.decode('utf-8')
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
                messages.success(request, 'User created successfully', extra_tags='success')
                return redirect(self.next_page_home)
            elif expiration_time < current_time:
                self.redis_client.delete(code_instance)
                messages.error(request, 'Code is expired', extra_tags='error')
                return redirect(self.next_page_login_verify_code)
        else:
            messages.error(request, 'Code is not valid', extra_tags='error')
            return redirect(self.next_page_login_verify_code)


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
        self.template_change_password = 'account/update/change_password.html'  # noqa
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
            messages.success(request, 'Your password was successfully updated!')
            return redirect(self.next_page_home)
        return render(request, self.template_change_password, {'form': form})


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
        self.template_login_email = 'account/login/login_email.html'  # noqa
        self.code_generator = CodeGenerator()  # noqa
        return super().setup(request, *args, **kwargs)

    def send_otp_email(self, email, otp):

        user = forms.User.objects.get(email=email)
        if user:
            subject = 'Your OTP for Verification'
            message = f'Your OTP for login is (Expiry date two minutes): {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(self.request, 'Code sent to your Email', extra_tags='success')
        elif not user:
            messages.success(self.request, 'Invalid email or password', extra_tags='success')
            return redirect(self.next_page_login_email)
        else:
            messages.success(self.request, 'Invalid email or password', extra_tags='success')
            return redirect(self.next_page_login_email)

    def get(self, request):
        return render(request, self.template_login_email, {'form': self.form_class()})

    def post(self, request):
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
                messages.error(request, 'Invalid email or password', extra_tags='error')
                return redirect(self.next_page_login_email)

        return render(request, self.template_login_email, {'form': form})


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
        self.template_verifycode = 'account/login/verify_code.html'  # noqa
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
                stored_code = code_instance.decode('utf-8')
                if not code_instance:
                    messages.error(request, 'Please Try again', extra_tags='error')

                current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
                expiration_time = current_time + timezone.timedelta(minutes=2)
                if request.POST['code'] == stored_code and expiration_time > current_time:  # noqa
                    user = user.first()  # noqa
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.ACCESS_TOKEN)
                    update_user_auth_uuid(user_id=request.user.id, token_type=UserAuth.REFRESH_TOKEN)
                    self.redis_client.delete(code_instance)
                    messages.success(request, 'Code verified successfully', extra_tags='success')
                    return redirect(self.next_page_success_login)
                elif expiration_time < current_time:
                    messages.error(request, 'Code is expired', extra_tags='error')
                    self.redis_client.delete(code_instance)
                    return redirect(self.next_page_login_email)
            else:
                messages.error(request, 'Code is not a valid', extra_tags='error')
                return redirect(self.next_page_login_verify_code)
        else:
            messages.error(request, 'Code is not valid', extra_tags='error')
            return redirect(self.next_page_login_verify_code)


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
    template_name = 'account/email/email_reset.html'
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
    template_name = 'account/email/email_reset_done.html'
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
    template_name = 'account/email/email_reset_confirm.html'
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
    template_name = 'account/email/email_reset_complete.html'
    http_method_names = ['get']


class UserChangeView(MustBeLogingCustomView):
    """
    View for changing user information.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form_class, next_page_home, next_page_change_user, user_instance, template name.
        Set up method to retrieve the current user instance.
        """
        self.form_class = forms.CustomUserChangeForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_change_user = reverse_lazy('change_user')  # noqa
        self.template_change_user = 'account/update/change_info_user.html'  # noqa
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
            messages.success(request, 'User information updated successfully', extra_tags='success')
            return redirect(self.next_page_home)
        return render(request, self.template_change_user, {'form': form})


class CreateProfileView(MustBeLogingCustomView):
    """
    Handles the creation of user profiles.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form, next page1, page2, template name.
        """
        self.form_class = forms.ProfileCreateForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_create_profile = reverse_lazy('create_profile')  # noqa
        self.template_create_profile = 'account/create/create_profile.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        Renders the form for creating a user profile.
        """
        form = self.form_class(instance=request.user)
        return render(request, self.template_create_profile, {'form': form})

    def post(self, request):
        """
        Handles form submission for creating a user profile.
        """
        try:
            profile = request.user.profile
        except forms.Profile.DoesNotExist:
            profile = None

        form = self.form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()
            messages.success(
                request,
                'Your profile has been created successfully',
                extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(
                request,
                'Your profile has not been created successfully',
                extra_tags='error')
            return redirect(self.next_page_create_profile)


class CreateAddressView(MustBeLogingCustomView):
    """
    Handles the creation of user addresses.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form, next page1, page2, template name.
        """
        self.form_class = forms.CreateAddressForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_create_address = reverse_lazy('create_address')  # noqa
        self.template_create_address = 'account/create/create_address.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        Renders the form for creating a user address.
        """
        addresses = request.user.address_set.all()  # Retrieve the user's addresses
        form = self.form_class(initial={'addresses': addresses})  # Pass the addresses to the form
        return render(request, self.template_create_address, {'form': form})

    def post(self, request):
        """
        Handles form submission for creating a user address.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(
                request,
                'Your address has been created successfully',
                extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(
                request,
                'Your address has not been created successfully',
                extra_tags='error')
            return redirect(self.next_page_create_address)


class ProfileDetailView(DetailView, MustBeLogingCustomView):
    http_method_names = ['get']
    model = forms.Profile  # Set the model

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'profile'
        self.template_name = 'account/profile/profile.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        addresses = forms.Address.objects.filter(user=self.request.user)

        context['profile'] = profile

        context['addresses'] = addresses

        return context


class DeleteUserView(DetailView, MustBeLogingCustomView):
    """
    View for displaying user details and providing an option for soft deletion.
    """
    model = User
    template_name = 'account/delete/delete_user.html'

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
        messages.success(request, 'User has been successfully soft deleted.')
        return redirect('home')
