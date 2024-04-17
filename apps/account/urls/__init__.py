from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.account.urls.api")),
    path("template/", include("apps.account.urls.template")),
]