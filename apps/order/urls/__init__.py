from django.urls import path, include

"""
This code snippet defines the `urlpatterns` list for routing URLs in a Django project.
- The `urlpatterns` list contains two `path` function calls:
  - `path("", include("apps.order.urls.urls_api"))`: This includes all URL patterns defined in the 
  `apps.order.urls.urls_api` module. The `""` as the path prefix means these patterns will be included directly 
  under the root URL.
  - `path("", include("apps.order.urls.urls_template"))`: This includes all URL patterns defined in the
   `apps.order.urls.urls_template` module. Similarly, the `""` as the path prefix means these patterns will also be 
   included directly under the root URL.
- The `include()` function allows including other URL configurations from specified modules (`urls_api` and 
`urls_template` in this case).
- This approach helps to organize URL routing by separating API-related and template-related URLs into different 
modules (`urls_api.py` and `urls_template.py` within the `apps.order.urls` package).
This setup enables the Django application to handle requests directed to different parts of the application based
 on the included URL patterns.
"""
urlpatterns = [
    path("", include("apps.order.urls.urls_api")),
    path("", include("apps.order.urls.urls_template")),
]
