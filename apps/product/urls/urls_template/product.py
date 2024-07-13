from django.urls import path
from apps.product.views.views_template import views_product

"""
Defines Django URL patterns for managing product-related operations using views from the `views_product` module.
- `path('product-create/', views_product.ProductCreateView.as_view(), name='product_create')`:
  Maps to a view (`ProductCreateView`) that handles creating new products. The URL pattern is named 'product_create'.
- `path('admin-seller-product-list/', views_product.AdminOrSellerProductListView.as_view(),
 name='admin_or_seller_product_list')`:
  Maps to a view (`AdminOrSellerProductListView`) that lists all products. The URL pattern is named 'admin_or_seller_product_list'.
- `path('product-detail/<int:pk>/', views_product.ProductDetailView.as_view(), name='product_detail')`:
  Maps to a view (`ProductDetailView`) that shows details of a specific product identified by `pk`. The URL pattern
   is named 'product_detail'.
- `path('product-update/<int:pk>/', views_product.ProductUpdateView.as_view(), name='product_update')`:
  Maps to a view (`ProductUpdateView`) that handles updating a product identified by `pk`. The URL pattern is named
   'product_update'.
- `path('product-delete/<int:pk>/', views_product.ProductDeleteView.as_view(), name='product_delete')`:
  Maps to a view (`ProductDeleteView`) that handles deleting a product identified by `pk`. The URL pattern is named
   'product_delete'.
Each `path()` function associates a URL endpoint with a corresponding view class (`as_view()` method converts the
 class-based view to a callable view) from the `views_product` module, providing CRUD (Create, Read, Update, Delete)
  functionality for product management within a Django application.
"""
urlpatterns = [
    path('product-create/', views_product.ProductCreateView.as_view(), name='product_create'),
    path('admin-seller-product-list/', views_product.AdminOrSellerProductListView.as_view(),
         name='admin_or_seller_product_list'),
    path('product-detail/<int:pk>/', views_product.ProductDetailView.as_view(), name='product_detail'),
    path('product-update/<int:pk>/', views_product.ProductUpdateView.as_view(), name='product_update'),
    path('product-delete/<int:pk>/', views_product.ProductDeleteView.as_view(), name='product_delete'),
]
