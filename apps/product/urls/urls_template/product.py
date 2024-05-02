from django.urls import path
from apps.product.views.views_template import views_product

urlpatterns = [

    path('product-create/', views_product.ProductCreateView.as_view(), name='product_create'),
    path('admin-seller-product-list/', views_product.AdminOrSellerProductListView.as_view(),
         name='admin_or_seller_product_list'),
    path('product-detail/<int:pk>/', views_product.ProductDetailView.as_view(), name='product_detail'),
    path('product-update/<int:pk>/', views_product.ProductUpdateView.as_view(), name='product_update'),
    path('product-delete/<int:pk>/', views_product.ProductDeleteView.as_view(), name='product_delete'),
]
