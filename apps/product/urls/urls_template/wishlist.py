from django.urls import path
from django.views.generic import TemplateView
from apps.product.views.views_template import views_wishlist


urlpatterns = [

    path('wishlist-add/<int:pk>/', views_wishlist.WishlistAddProductView.as_view(), name='wishlist_add'),
    path('wishlist-detail/', views_wishlist.WishlistShowProductView.as_view(), name='wishlist_detail'),
    path('show-wishlist-detail/', TemplateView.as_view(template_name='product/wishlist/wishlist.html'),
         name='show_wishlist-detail'),
    # path('wishlist-detail/<int:pk>/', views_wishlist.WishlistDetailView.as_view(), name='wishlist_detail'),
    path('wishlist-update/<int:pk>/', views_wishlist.WishlistUpdateProductView.as_view(), name='wishlist_update'),
    # path('wishlist-delete/<int:pk>/', views_wishlist.WishlistDeleteView.as_view(), name='wishlist_delete'),
]
