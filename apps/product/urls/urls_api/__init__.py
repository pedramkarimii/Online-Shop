from django.urls import path, include

"""
Defines the `urlpatterns` list, which maps URL patterns to respective applications or modules for API endpoints related to categories, brands, discounts, warehouse keepers, and wishlists.
- `path("", include("apps.product.urls.urls_api.category"))`: Includes URL patterns from the `urls_api.category` module under the `apps.product.urls` package.
- `path("", include("apps.product.urls.urls_api.brand"))`: Includes URL patterns from the `urls_api.brand` module under the `apps.product.urls` package.
- `path("", include("apps.product.urls.urls_api.discount"))`: Includes URL patterns from the `urls_api.discount` module under the `apps.product.urls` package.
- `path("", include("apps.product.urls.urls_api.warehouse_keeper"))`: Includes URL patterns from the `urls_api.warehouse_keeper` module under the `apps.product.urls` package.
- `path("", include("apps.product.urls.urls_api.wishlist"))`: Includes URL patterns from the `urls_api.wishlist` module under the `apps.product.urls` package.
These patterns are included at the root level (`""`) of the URL configuration.
"""
urlpatterns = [
    path("", include("apps.product.urls.urls_api.category")),
    path("", include("apps.product.urls.urls_api.brand")),
    path("", include("apps.product.urls.urls_api.discount")),
    path("", include("apps.product.urls.urls_api.warehouse_keeper")),
    path("", include("apps.product.urls.urls_api.wishlist")),
]
