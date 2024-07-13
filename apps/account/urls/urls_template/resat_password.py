from django.urls import path
from apps.account.views.views_template import views_resat_password

"""
URL configuration for password reset-related views:
- "resat-password/": Maps to UserPasswordResetView for initiating a password reset request.
- "resat-password/done/": Maps to UserPasswordResetDoneView for displaying a message after initiating a password reset request.
- "confirm/<uidb64>/<token>/": Maps to UserPasswordResetConfirmView for confirming a password reset using a UID and token.
- "confirm/resat-complete/": Maps to UserPasswordResetCompleteView for displaying a message after completing a password reset.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
urlpatterns = [
    path("resat-password/", views_resat_password.UserPasswordResetView.as_view(), name="resat_password"),
    path("resat-password/done/", views_resat_password.UserPasswordResetDoneView.as_view(), name="resat_done"),
    path("confirm/<uidb64>/<token>/", views_resat_password.UserPasswordResetConfirmView.as_view(),
         name="resat_password_confirm"),
    path("confirm/resat-complete/", views_resat_password.UserPasswordResetCompleteView.as_view(),
         name="resat_complete"),
]
