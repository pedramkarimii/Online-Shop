from django.urls import path, include

urlpatterns = [
    # path("", include("apps.product.urls.urls_bucket.product")),
    path("", include("apps.product.urls.urls_bucket.category")),
    path("", include("apps.product.urls.urls_bucket.brand")),
    path("", include("apps.product.urls.urls_bucket.discount")),
    path("", include("apps.product.urls.urls_bucket.warehouse_keeper")),
]
