from django.urls import path, include

urlpatterns = [
    path("api/", include("apps.core.urls.api")),
    path("template/", include("apps.core.urls.template")),
]