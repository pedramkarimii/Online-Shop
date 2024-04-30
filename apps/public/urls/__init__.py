from django.urls import path, include


urlpatterns = [
    path("", include("apps.public.urls.urls_api")),
    path("", include("apps.public.urls.urls_template")),
    path("", include("apps.public.urls.urls_bucket")),
]