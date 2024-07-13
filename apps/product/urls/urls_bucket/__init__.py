from django.urls import path, include

"""
Defines the `urlpatterns` list, which includes various URL patterns imported from different modules within the 
`apps.product.urls.urls_bucket` package. 
- `path("", include("apps.product.urls.urls_bucket.category"))`: Includes URL patterns from the `urls_bucket.category`
 module, allowing navigation to category-related endpoints.
- `path("", include("apps.product.urls.urls_bucket.brand"))`: Includes URL patterns from the `urls_bucket.brand`
 module, facilitating navigation to brand-related endpoints.
- `path("", include("apps.product.urls.urls_bucket.discount"))`: Includes URL patterns from the `urls_bucket.discount` 
module, providing access to discount-related endpoints.
- `path("", include("apps.product.urls.urls_bucket.warehouse_keeper"))`: Includes URL patterns from the 
`urls_bucket.warehouse_keeper` module, enabling navigation to endpoints related to warehouse management.
Each `include()` function call includes the entire set of URL patterns defined in the respective modules, allowing for
 modular and organized URL routing within the Django project. This approach helps in maintaining separation of 
 concerns and scalability in the project structure.
"""
urlpatterns = [
    path("", include("apps.product.urls.urls_bucket.category")),
    path("", include("apps.product.urls.urls_bucket.brand")),
    path("", include("apps.product.urls.urls_bucket.discount")),
    path("", include("apps.product.urls.urls_bucket.warehouse_keeper")),
]
