from django.urls import path, include


urlpatterns = [
    path("", include("apps.order.urls.urls_api")),
    path("", include("apps.order.urls.urls_template")),
]