from django.urls import path, include

"""
This code defines the URL patterns for a Django project by including URL configurations 
from specific modules within the "apps.public.urls.urls_template" package. These modules 
("login" and "home") contain their own sets of URL patterns that are integrated into the main project.

1. `path("", include("apps.public.urls.urls_template.login"))`:
   - Includes all URL patterns defined in `apps.public.urls.urls_template.login`.
   - These routes are added at the root level, meaning they will be matched directly 
     from the base URL of the site.

2. `path("", include("apps.public.urls.urls_template.home"))`:
   - Includes all URL patterns defined in `apps.public.urls.urls_template.home`.
   - These routes are also added at the root level, similar to the login routes.

By using `include()`, it allows for a modular organization of URL patterns, 
making it easier to manage and maintain the routes for different parts of the application.
"""
urlpatterns = [
    path("", include("apps.public.urls.urls_template.login")),
    path("", include("apps.public.urls.urls_template.home")),
]
