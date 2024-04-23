from django.urls import path
from apps.account.views import views_template

urlpatterns = [
    # Authentication URLs
    # These URLs handle user authentication, such as logging in, logging out, and verifying successful login.
    path("login/", views_template.UserLoginUsernameOrEmailView.as_view(), name="login"),
    path("login-phone-number/", views_template.UserLoginPhoneNumberView.as_view(), name="login_phone_number"),
    path("login-email/", views_template.UserLoginEmailView.as_view(), name="login_email"),
    path("success-login/", views_template.SuccessLoginView.as_view(), name="success_login"),
    path("logout/", views_template.UserLogoutView.as_view(), name="logout"),
    # Registration URLs
    # These URLs handle user registration and verification of registration codes.
    path('register/', views_template.UserRegisterView.as_view(), name='register_user'),
    path('verify/', views_template.UserRegistrationVerifyCodeView.as_view(), name='verify_code'),
    path('login-verify/', views_template.LoginVerifyCodeView.as_view(), name='login_verify_code'),
    path('login-verify-email/', views_template.LoginVerifyCodeEmailView.as_view(), name='login_verify_code_email'),
    # Account Management URLs
    # These URLs handle user account management,such as changing user information,changing passwords,and deleting users.
    path('change-user/', views_template.UserChangeView.as_view(), name='change_user'),
    path("change-password/", views_template.ChangePasswordView.as_view(), name="change_pass"),
    path('users/<int:pk>/delete/', views_template.DeleteUserView.as_view(), name='delete_user'),
    # Profile Management URLs
    # These URLs handle user profile management, such as creating profiles, viewing profiles, and deleting profiles.
    path("profiles/<int:pk>/", views_template.ProfileDetailView.as_view(), name="profile_detail"),
    path("create-profile/", views_template.CreateProfileView.as_view(), name="create_profile"),
    path("create-address/", views_template.CreateAddressView.as_view(), name="create_address"),
    # Password Reset URLs
    # These URLs handle password reset functionality, such as requesting password resets, confirming password resets,
    # and completing password resets.
    path("resat-password/", views_template.UserPasswordResetView.as_view(), name="resat_password"),
    path("resat-password/done/", views_template.UserPasswordResetDoneView.as_view(), name="resat_done"),
    path("confirm/<uidb64>/<token>/", views_template.UserPasswordResetConfirmView.as_view(),
         name="resat_password_confirm"),
    path("confirm/resat-complete/", views_template.UserPasswordResetCompleteView.as_view(), name="resat_complete"),

]
