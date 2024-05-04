from django.urls import path
from apps.account.views.views_template import views_role

urlpatterns = [
    path('role-create/', views_role.RoleCreateView.as_view(), name='role_create'),
    path('admin-role-list/', views_role.AdminRoleListView.as_view(),
         name='admin_role_list'),
    path('role-detail/<int:pk>/', views_role.RoleDetailView.as_view(), name='role_detail'),
    path('role-update/<int:pk>/', views_role.RoleUpdateView.as_view(), name='role_update'),
    path('role-delete/<int:pk>/', views_role.RoleDeleteView.as_view(), name='role_delete'),
]
