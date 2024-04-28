from django.urls import path
from apps.account.views.views_template import views_auth

urlpatterns = [
    path('register/', views_auth.UserRegisterView.as_view(), name='user_create'),
    path('verify/', views_auth.UserRegistrationVerifyCodeView.as_view(), name='verify_code'),
    path('login-verify/', views_auth.LoginVerifyCodeView.as_view(), name='login_verify_code'),
    path('login-verify-email/', views_auth.LoginVerifyCodeEmailView.as_view(), name='login_verify_code_email'),
]
