from django.urls import path
from apps.public.views.views_template import views_login

urlpatterns = [
    path("login/", views_login.UserLoginUsernameOrEmailView.as_view(), name="login"),
    path("login-phone-number/", views_login.UserLoginPhoneNumberView.as_view(), name="login_phone_number"),
    path("login-email/", views_login.UserLoginEmailView.as_view(), name="login_email"),
    path("success-login/", views_login.SuccessLoginView.as_view(), name="success_login"),
    path("logout/", views_login.UserLogoutView.as_view(), name="logout"),
]

