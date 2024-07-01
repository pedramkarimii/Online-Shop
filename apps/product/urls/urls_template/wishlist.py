from django.urls import path
from django.views.generic import TemplateView
from apps.product.views.views_template import views_wishlist

"""
Defines Django URL patterns for wishlist-related operations using views from the `views_wishlist` module.
- `path('wishlist-add/<int:pk>/', views_wishlist.WishlistAddProductView.as_view(), name='wishlist_add')`:
  Maps to a view (`WishlistAddProductView`) that handles adding products to a wishlist identified by `pk`.
  The URL pattern is named 'wishlist_add'.
- `path('wishlist-detail/', views_wishlist.WishlistShowProductView.as_view(), name='wishlist_detail')`:
  Maps to a view (`WishlistShowProductView`) that displays the wishlist details. The URL pattern
   is named 'wishlist_detail'.
- `path('show-wishlist-detail/', TemplateView.as_view(template_name='product/wishlist/wishlist.html'),
 name='show_wishlist-detail')`:
  Maps to a template view (`TemplateView`) that renders a static HTML template (`wishlist.html`)
   to show wishlist details.
  The URL pattern is named 'show_wishlist-detail'.
- `path('wishlist-update/<int:pk>/', views_wishlist.WishlistUpdateProductView.as_view(), name='wishlist_update')`:
  Maps to a view (`WishlistUpdateProductView`) that handles updating products in the wishlist identified by `pk`.
  The URL pattern is named 'wishlist_update'.
- `path('wishlist-delete/<int:pk>/', views_wishlist.WishlistDeleteProductView.as_view(), name='wishlist_delete')`:
  Maps to a view (`WishlistDeleteProductView`) that handles deleting products from the wishlist identified by `pk`.
  The URL pattern is named 'wishlist_delete'.

Each `path()` function associates a URL endpoint with a corresponding view class or template view, providing wishlist
 management functionality within a Django application.
"""
urlpatterns = [
    path('wishlist-add/<int:pk>/', views_wishlist.WishlistAddProductView.as_view(), name='wishlist_add'),
    path('wishlist-detail/', views_wishlist.WishlistShowProductView.as_view(), name='wishlist_detail'),
    path('show-wishlist-detail/', TemplateView.as_view(template_name='product/wishlist/wishlist.html'),
         name='show_wishlist-detail'),
    path('wishlist-update/<int:pk>/', views_wishlist.WishlistUpdateProductView.as_view(), name='wishlist_update'),
    path('wishlist-delete/<int:pk>/', views_wishlist.WishlistDeleteProductView.as_view(), name='wishlist_delete'),
]
