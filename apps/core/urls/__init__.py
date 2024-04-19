from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.core.urls.urls_api")),
    path("template/", include("apps.core.urls.urls_template")),
]