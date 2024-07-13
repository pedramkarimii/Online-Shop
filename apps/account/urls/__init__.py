from django.urls import path, include

"""
Main URL configuration for the project:
- "": Includes URLs from "apps.account.urls.urls_api" for API endpoints.
- "": Includes URLs from "apps.account.urls.urls_template" for template-based views.
This setup allows organizing URL patterns into separate modules for API endpoints and template views.
"""
urlpatterns = [
    path("", include("apps.account.urls.urls_api")),
    path("", include("apps.account.urls.urls_template")),
]
