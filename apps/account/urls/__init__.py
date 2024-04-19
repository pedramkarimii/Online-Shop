from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.account.urls.urls_api")),
    path("template/", include("apps.account.urls.urls_template")),
]