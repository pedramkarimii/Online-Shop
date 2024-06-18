from django.urls import path
from apps.account.views.views_template import views_discount

urlpatterns = [
    path('discount-cod-create/', views_discount.DiscountCodCreateView.as_view(), name='discount_cod_create'),
    path('admin-discount-cod-list/', views_discount.AdminDiscountCodDetailView.as_view(),
         name='admin_discount_cod_list'),
    path('discount-cod-detail/<int:pk>/', views_discount.DiscountCodDetailView.as_view(), name='discount_cod_detail'),
    path('discount-cod-update/<int:pk>/', views_discount.DiscountCodUpdateView.as_view(), name='discount_cod_update'),
    path('discount-cod-delete/<int:pk>/', views_discount.DiscountCodDeleteView.as_view(), name='discount_cod_delete'),
    path('discount-cod-wishlist/', views_discount.WishlistDiscountCodProductView.as_view(),
         name='discount_cod_wishlist'),
]
