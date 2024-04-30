from django.urls import path
from apps.account.views.views_template import views_user

urlpatterns = [
    path('user-update/', views_user.UserUpdateView.as_view(), name='user_update'),
    path("user-change-password/", views_user.ChangePasswordView.as_view(), name="user_change_password"),
    path('user/delete/<int:pk>/', views_user.UserDeleteView.as_view(), name='user_delete'),
]
