from django.urls import path
from apps.product.views.views_template import views_category

"""
Defines Django URL patterns for managing category-related operations using views from the `views_category` module.
- `path('category-create/', views_category.CategoryCreateView.as_view(), name='category_create')`:
  Maps to a view (`CategoryCreateView`) that handles creating new category entries. The URL pattern is named 
  'category_create'.
- `path('admin-category-list/', views_category.AdminCategoryListView.as_view(), name='admin_category_list')`:
  Maps to a view (`AdminCategoryListView`) that lists all category entries. The URL pattern is named 
  'admin_category_list'.
- `path('category-detail/<int:pk>/', views_category.CategoryDetailView.as_view(), name='category_detail')`:
  Maps to a view (`CategoryDetailView`) that shows details of a specific category entry identified by `pk`. 
  The URL pattern is named 'category_detail'.
- `path('category-update/<int:pk>/', views_category.CategoryUpdateView.as_view(), name='category_update')`:
  Maps to a view (`CategoryUpdateView`) that handles updating a category entry identified by `pk`. The URL pattern
   is named 'category_update'.
- `path('category-delete/<int:pk>/', views_category.CategoryDeleteView.as_view(), name='category_delete')`:
  Maps to a view (`CategoryDeleteView`) that handles deleting a category entry identified by `pk`. The URL pattern
   is named 'category_delete'.
Each `path()` function associates a URL endpoint with a corresponding view class (`as_view()` method converts the
 class-based view to a callable view) from the `views_category` module, providing CRUD (Create, Read, Update, Delete)
  functionality for category management within a Django application.
"""

urlpatterns = [
    path('category-create/', views_category.CategoryCreateView.as_view(), name='category_create'),
    path('admin-category-list/', views_category.AdminCategoryListView.as_view(), name='admin_category_list'),
    path('category-detail/<int:pk>/', views_category.CategoryDetailView.as_view(), name='category_detail'),
    path('category-update/<int:pk>/', views_category.CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', views_category.CategoryDeleteView.as_view(), name='category_delete'),
]
