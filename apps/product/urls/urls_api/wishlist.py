from django.urls import path
from apps.product.views.api import api_wishlist

"""
Defines the `urlpatterns` list, which maps specific URL patterns to corresponding views in the `api_wishlist` module for managing wishlist-related API endpoints.
- `path('wishlists-add/<int:pk>/', api_wishlist.WishlistAddProductAPI.as_view(), name='wishlist_add_api')`: Maps the URL pattern `wishlists-add/<int:pk>/` to the `WishlistAddProductAPI` view class for adding products to a wishlist, with `pk` as a parameter.
- `path('wishlists-detail/<int:pk>/', api_wishlist.WishlistShowProductAPI.as_view(), name='wishlist_detail_api')`: Maps the URL pattern `wishlists-detail/<int:pk>/` to the `WishlistShowProductAPI` view class for showing details of a product in a wishlist, with `pk` as a parameter.
- `path('wishlists-update/<int:pk>/', api_wishlist.WishlistUpdateProductAPI.as_view(), name='wishlist_update_api')`: Maps the URL pattern `wishlists-update/<int:pk>/` to the `WishlistUpdateProductAPI` view class for updating products in a wishlist, with `pk` as a parameter.
- `path('wishlists-delete/<int:pk>/', api_wishlist.WishlistDeleteProductAPI.as_view(), name='wishlist_delete_api')`: Maps the URL pattern `wishlists-delete/<int:pk>/` to the `WishlistDeleteProductAPI` view class for deleting products from a wishlist, with `pk` as a parameter.
- `path('wishlists-discount-cod/', api_wishlist.WishlistDiscountCodProductAPI.as_view(), name='wishlist_discount_cod_api')`: Maps the URL pattern `wishlists-discount-cod/` to the `WishlistDiscountCodProductAPI` view class for applying discounts to products in a wishlist.
Each `path()` function call specifies the URL pattern, the corresponding view class (`as_view()` method is used to convert the view class into a view function), and a unique name for easy URL referencing in Django templates or code.
"""
urlpatterns = [

    path('wishlists-add/<int:pk>/', api_wishlist.WishlistAddProductAPI.as_view(), name='wishlist_add_api'),
    path('wishlists-detail/<int:pk>/', api_wishlist.WishlistShowProductAPI.as_view(), name='wishlist_detail_api'),
    path('wishlists-update/<int:pk>/', api_wishlist.WishlistUpdateProductAPI.as_view(), name='wishlist_update_api'),
    path('wishlists-delete/<int:pk>/', api_wishlist.WishlistDeleteProductAPI.as_view(), name='wishlist_delete_api'),
    path('wishlists-discount-cod/', api_wishlist.WishlistDiscountCodProductAPI.as_view(),
         name='wishlist_discount_cod_api'),
]
