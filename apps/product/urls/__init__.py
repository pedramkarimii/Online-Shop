from django.urls import path, include


urlpatterns = [
    path("", include("apps.product.urls.urls_api")),
    path("", include("apps.product.urls.urls_template")),
    path("", include("apps.product.urls.urls_bucket")),
]