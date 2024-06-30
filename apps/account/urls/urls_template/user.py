from django.urls import path
from apps.account.views.views_template import views_user

"""
URL configuration for user-related views:
- "user-update/<int:pk>/": Maps to UserUpdateView for updating user information by their primary key.
- "user-change-password/": Maps to ChangePasswordView for allowing users to change their password.
- "user/delete/<int:pk>/": Maps to UserDeleteView for deleting a user by their primary key.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
urlpatterns = [
    path('user-update/<int:pk>/', views_user.UserUpdateView.as_view(), name='user_update'),
    path("user-change-password/", views_user.ChangePasswordView.as_view(), name="user_change_password"),
    path('user/delete/<int:pk>/', views_user.UserDeleteView.as_view(), name='user_delete'),
]
