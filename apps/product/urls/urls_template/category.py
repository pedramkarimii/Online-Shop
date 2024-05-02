from django.urls import path
from apps.product.views.views_template import views_category

urlpatterns = [
    path('category-create/', views_category.CategoryCreateView.as_view(), name='category_create'),
    path('admin-category-list/', views_category.AdminCategoryListView.as_view(), name='admin_category_list'),
    path('category-detail/<int:pk>/', views_category.CategoryDetailView.as_view(), name='category_detail'),
    path('category-update/<int:pk>/', views_category.CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', views_category.CategoryDeleteView.as_view(), name='category_delete'),
]
