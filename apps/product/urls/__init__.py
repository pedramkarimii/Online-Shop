from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.product.urls.api")),
    path("template/", include("apps.product.urls.template")),
]