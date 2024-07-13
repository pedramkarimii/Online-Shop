from django.urls import path
from apps.product.views.views_template import views_brand

"""
Defines Django URL patterns for managing brand-related operations using views from the `views_brand` module.
- `path('brand-create/', views_brand.BrandCreateView.as_view(), name='brand_create')`:
  Maps to a view (`BrandCreateView`) that handles creating new brand entries. The URL pattern is named 'brand_create'.
- `path('admin-seller-brand-list/', views_brand.AdminOrSellerBrandListView.as_view(),
 name='admin_or_seller_brand_list')`:
  Maps to a view (`AdminOrSellerBrandListView`) that lists all brand entries. The URL pattern 
  is named 'admin_or_seller_brand_list'.
- `path('brand-detail/<int:pk>/', views_brand.BrandDetailView.as_view(), name='brand_detail')`:
  Maps to a view (`BrandDetailView`) that shows details of a specific brand entry identified by `pk`. 
  The URL pattern is named 'brand_detail'.
- `path('brand-update/<int:pk>/', views_brand.BrandUpdateView.as_view(), name='brand_update')`:
  Maps to a view (`BrandUpdateView`) that handles updating a brand entry identified by `pk`. The URL pattern 
  is named 'brand_update'.
- `path('brand-delete/<int:pk>/', views_brand.BrandDeleteView.as_view(), name='brand_delete')`:
  Maps to a view (`BrandDeleteView`) that handles deleting a brand entry identified by `pk`. The URL pattern 
  is named 'brand_delete'.
Each `path()` function associates a URL endpoint with a corresponding view class (`as_view()` method converts 
the class-based view to a callable view) from the `views_brand` module, providing CRUD (Create, Read, Update, Delete)
 functionality for brand management within a Django application.
"""
urlpatterns = [
    path('brand-create/', views_brand.BrandCreateView.as_view(), name='brand_create'),
    path('admin-seller-brand-list/', views_brand.AdminOrSellerBrandListView.as_view(),
         name='admin_or_seller_brand_list'),
    path('brand-detail/<int:pk>/', views_brand.BrandDetailView.as_view(), name='brand_detail'),
    path('brand-update/<int:pk>/', views_brand.BrandUpdateView.as_view(), name='brand_update'),
    path('brand-delete/<int:pk>/', views_brand.BrandDeleteView.as_view(), name='brand_delete'),
]
