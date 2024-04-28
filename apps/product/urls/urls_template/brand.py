from django.urls import path
from apps.product.views.views_template import views_brand
urlpatterns = [
    path('brand-create/', views_brand.BrandCreateView.as_view(), name='brand_create'),
    # path('brand-detail/<int:pk>/', views_product.BrandDetailView.as_view(), name='brand_detail'),
    path('brand-update/<int:pk>/', views_brand.BrandUpdateView.as_view(), name='brand_update'),
    path('brand-delete/<int:pk>/', views_brand.BrandDeleteView.as_view(), name='brand_delete'),
]
