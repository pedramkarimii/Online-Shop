from django.urls import path, include

"""
Defines Django URL patterns for modular inclusion of product-related URLs.
- `path("", include("apps.product.urls.urls_api"))`:
  Includes URLs from the `urls_api` module under `apps.product.urls`. These URLs typically handle API endpoints
  related to product management, such as CRUD operations.
- `path("", include("apps.product.urls.urls_template"))`:
  Includes URLs from the `urls_template` module under `apps.product.urls`. These URLs are usually used for rendering
  templates and managing product-related views within the Django application.
- `path("", include("apps.product.urls.urls_bucket"))`:
  Includes URLs from the `urls_bucket` module under `apps.product.urls`, which might handle bucket-related operations
  if applicable to the product management context.
Each `path()` function call uses the `include()` function to integrate the specified module's URLs into the current 
URL configuration,
allowing for modular and organized routing of product-related functionalities in a Django project.
"""
urlpatterns = [
    path("", include("apps.product.urls.urls_api")),
    path("", include("apps.product.urls.urls_template")),
    path("", include("apps.product.urls.urls_bucket")),
]
