from django.urls import path
from apps.account.views.views_template import views_role

"""
URL configuration for role-related views:
- "role-create/": Maps to RoleCreateView for creating a new role.
- "admin-role-list/": Maps to AdminRoleListView for listing roles (admin view).
- "role-detail/<int:pk>/": Maps to RoleDetailView for viewing a role by its primary key.
- "role-update/<int:pk>/": Maps to RoleUpdateView for updating a role by its primary key.
- "role-delete/<int:pk>/": Maps to RoleDeleteView for deleting a role by its primary key.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
urlpatterns = [
    path('role-create/', views_role.RoleCreateView.as_view(), name='role_create'),
    path('admin-role-list/', views_role.AdminRoleListView.as_view(),
         name='admin_role_list'),
    path('role-detail/<int:pk>/', views_role.RoleDetailView.as_view(), name='role_detail'),
    path('role-update/<int:pk>/', views_role.RoleUpdateView.as_view(), name='role_update'),
    path('role-delete/<int:pk>/', views_role.RoleDeleteView.as_view(), name='role_delete'),
]
