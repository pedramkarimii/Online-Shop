from django.urls import path
from apps.product.views.api import api_wishlist

urlpatterns = [

    path('wishlists-add/<int:pk>/', api_wishlist.WishlistAddProductAPI.as_view(), name='wishlist_add_api'),
    path('wishlists-detail/<int:pk>/', api_wishlist.WishlistShowProductAPI.as_view(), name='wishlist_detail_api'),
    path('wishlists-update/<int:pk>/', api_wishlist.WishlistUpdateProductAPI.as_view(), name='wishlist_update_api'),
    path('wishlists-delete/<int:pk>/', api_wishlist.WishlistDeleteProductAPI.as_view(), name='wishlist_delete_api'),
    path('wishlists-discount-cod/', api_wishlist.WishlistDiscountCodProductAPI.as_view(),
         name='wishlist_discount_cod_api'),
]
