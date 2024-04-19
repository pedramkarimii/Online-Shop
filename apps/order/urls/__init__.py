from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.order.urls.urls_api")),
    path("template/", include("apps.order.urls.urls_template")),
]