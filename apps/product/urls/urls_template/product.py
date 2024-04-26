from django.urls import path
from apps.product.views import views_template

urlpatterns = [

    path('product-create/', views_template.ProductCreateView.as_view(), name='product_create'),
    # path('product-detail/<int:pk>/', views_template.ProductDetailView.as_view(), name='product_detail'),
    path('product-update/<int:pk>/', views_template.ProductUpdateView.as_view(), name='product_update'),
    path('product-delete/<int:pk>/', views_template.ProductDeleteView.as_view(), name='product_delete'),
]
