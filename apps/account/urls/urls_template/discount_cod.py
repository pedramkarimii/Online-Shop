from django.urls import path
from apps.account.views.views_template import views_discount

"""
URL configuration for discount-related views:
- "discount-cod-create/": Maps to DiscountCodCreateView for creating a new discount code.
- "admin-discount-cod-list/": Maps to AdminDiscountCodDetailView for listing discount codes for admin.
- "discount-cod-detail/<int:pk>/": Maps to DiscountCodDetailView for viewing a discount code by its primary key.
- "discount-cod-update/<int:pk>/": Maps to DiscountCodUpdateView for updating a discount code by its primary key.
- "discount-cod-delete/<int:pk>/": Maps to DiscountCodDeleteView for deleting a discount code by its primary key.
- "discount-cod-wishlist/": Maps to WishlistDiscountCodProductView for listing discount codes in the wishlist.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
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
