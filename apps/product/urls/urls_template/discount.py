from django.urls import path
from apps.product.views import views_template

urlpatterns = [
    path('discount-create/', views_template.DiscountCreateView.as_view(), name='discount_create'),
    # path('discount-detail/<int:pk>/', views_template.DiscountDetailView.as_view(), name='discount_detail'),
    path('discount-update/<int:pk>/', views_template.DiscountUpdateView.as_view(), name='discount_update'),
    path('discount-delete/<int:pk>/', views_template.DiscountDeleteView.as_view(), name='discount_delete'),
]
