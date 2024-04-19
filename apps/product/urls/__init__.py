from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.product.urls.urls_api")),
    path("template/", include("apps.product.urls.urls_template")),
]