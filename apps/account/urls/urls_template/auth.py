from django.urls import path
from apps.account.views.views_template import views_auth

"""
URL configuration for authentication-related views:
- "register/": Maps to UserRegisterView for registering a new user.
- "verify/": Maps to UserRegistrationVerifyCodeView for verifying user registration via a code.
- "login-verify/": Maps to LoginVerifyCodeView for verifying user login via a code.
- "login-verify-email/": Maps to LoginVerifyCodeEmailView for verifying user login via an email code.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
urlpatterns = [
    path('register/', views_auth.UserRegisterView.as_view(), name='user_create'),
    path('verify/', views_auth.UserRegistrationVerifyCodeView.as_view(), name='verify_code'),
    path('login-verify/', views_auth.LoginVerifyCodeView.as_view(), name='login_verify_code'),
    path('login-verify-email/', views_auth.LoginVerifyCodeEmailView.as_view(), name='login_verify_code_email'),
]
