from django.urls import path, include

urlpatterns = [
    # path("", include("apps.product.urls.urls_api.product")),
    path("", include("apps.product.urls.urls_api.category")),
    path("", include("apps.product.urls.urls_api.brand")),
    path("", include("apps.product.urls.urls_api.discount")),
    path("", include("apps.product.urls.urls_api.warehouse_keeper")),
    path("", include("apps.product.urls.urls_api.wishlist")),
]
