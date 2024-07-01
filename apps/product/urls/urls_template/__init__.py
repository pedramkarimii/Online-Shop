from django.urls import path, include

"""
Defines the `urlpatterns` list, which includes various URL patterns imported from different modules within the 
`apps.product.urls.urls_template` package.
- `path("", include("apps.product.urls.urls_template.product"))`: Integrates URL patterns from the `product`
 module under `urls_template`, enabling access to product-related endpoints.
- `path("", include("apps.product.urls.urls_template.comment"))`: Includes URL patterns from the `comment` 
module under `urls_template`, facilitating navigation to comment-related endpoints.
- `path("", include("apps.product.urls.urls_template.category"))`: Includes URL patterns from the `category` 
module under `urls_template`, providing access to category-related endpoints.
- `path("", include("apps.product.urls.urls_template.brand"))`: Integrates URL patterns from the `brand` 
module under `urls_template`, allowing navigation to brand-related endpoints.
- `path("", include("apps.product.urls.urls_template.discount"))`: Includes URL patterns from the `discount` 
module under `urls_template`, enabling access to discount-related endpoints.
- `path("", include("apps.product.urls.urls_template.add_to_inventory"))`: Integrates URL patterns from the 
`add_to_inventory` module under `urls_template`, facilitating navigation to endpoints related to adding inventory.
- `path("", include("apps.product.urls.urls_template.inventory"))`: Includes URL patterns from the `inventory` 
module under `urls_template`, providing access to inventory-related endpoints.
- `path("", include("apps.product.urls.urls_template.wishlist"))`: Integrates URL patterns from the `wishlist` 
module under `urls_template`, allowing navigation to wishlist-related endpoints.
Each `include()` function call imports and integrates the entire set of URL patterns defined in the respective modules. 
This approach organizes URL routing within the Django project by separating different aspects of product management 
into distinct modules, improving maintainability and scalability.
"""
urlpatterns = [
    path("", include("apps.product.urls.urls_template.product")),
    path("", include("apps.product.urls.urls_template.comment")),
    path("", include("apps.product.urls.urls_template.category")),
    path("", include("apps.product.urls.urls_template.brand")),
    path("", include("apps.product.urls.urls_template.discount")),
    path("", include("apps.product.urls.urls_template.add_to_inventory")),
    path("", include("apps.product.urls.urls_template.inventory")),
    path("", include("apps.product.urls.urls_template.wishlist")),
]
