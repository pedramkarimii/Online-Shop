from django.urls import path
from apps.product.views.api import api_wishlist

urlpatterns = [

    path('wishlists-add/<int:pk>/', api_wishlist.WishlistAddProductAPI.as_view(), name='wishlist_add_api'),
    # path('admin-seller-wishlist-list/', api_wishlist.AdminOrSellerProductListView.as_view(),
    #      name='admin_or_seller_wishlist_list'),
    path('wishlists-detail/<int:pk>/', api_wishlist.WishlistShowProductAPI.as_view(), name='wishlist_detail_api'),
    # path('wishlist-update/<int:pk>/', api_wishlist.WishlistUpdateView.as_view(), name='wishlist_update'),
    # path('wishlist-delete/<int:pk>/', api_wishlist.WishlistDeleteView.as_view(), name='wishlist_delete'),
]
