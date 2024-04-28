from django.urls import path
from apps.account.views.views_template import views_resat_password

urlpatterns = [
    path("resat-password/", views_resat_password.UserPasswordResetView.as_view(), name="resat_password"),
    path("resat-password/done/", views_resat_password.UserPasswordResetDoneView.as_view(), name="resat_done"),
    path("confirm/<uidb64>/<token>/", views_resat_password.UserPasswordResetConfirmView.as_view(),
         name="resat_password_confirm"),
    path("confirm/resat-complete/", views_resat_password.UserPasswordResetCompleteView.as_view(),
         name="resat_complete"),
]
