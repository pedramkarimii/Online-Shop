from django.urls import path, include

"""
This code defines the URL patterns for a Django project by including URL configurations 
from different modules within the "apps.public.urls" package. Each of these modules 
("urls_api", "urls_template", and "urls_bucket") contains its own set of URL patterns 
that are integrated into the main project.

1. `path("", include("apps.public.urls.urls_api"))`:
   - Includes all URL patterns defined in `apps.public.urls.urls_api`.
   - These routes are added at the root level, meaning they will be matched directly 
     from the base URL of the site.

2. `path("", include("apps.public.urls.urls_template"))`:
   - Includes all URL patterns defined in `apps.public.urls.urls_template`.
   - These routes are also added at the root level, similar to the API routes.

3. `path("", include("apps.public.urls.urls_bucket"))`:
   - Includes all URL patterns defined in `apps.public.urls.urls_bucket`.
   - These routes are similarly added at the root level.

By using `include()`, it allows for a modular organization of URL patterns, 
making it easier to manage and maintain the routes for different parts of the application.
"""
urlpatterns = [
    path("", include("apps.public.urls.urls_api")),
    path("", include("apps.public.urls.urls_template")),
    path("", include("apps.public.urls.urls_bucket")),
]
