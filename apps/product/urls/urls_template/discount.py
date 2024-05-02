from django.urls import path
from apps.product.views.views_template import views_discount_create

urlpatterns = [
    path('discount-create/', views_discount_create.DiscountCreateView.as_view(), name='discount_create'),
    path('admin-discount-list/', views_discount_create.AdminDiscountListView.as_view(), name='admin_discount_list'),
    path('discount-detail/<int:pk>/', views_discount_create.DiscountDetailView.as_view(), name='discount_detail'),
    path('discount-update/<int:pk>/', views_discount_create.DiscountUpdateView.as_view(), name='discount_update'),
    path('discount-delete/<int:pk>/', views_discount_create.DiscountDeleteView.as_view(), name='discount_delete'),
]
