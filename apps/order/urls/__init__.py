from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.order.urls.api")),
    path("template/", include("apps.order.urls.template")),
]