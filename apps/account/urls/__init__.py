from django.urls import path, include


urlpatterns = [
    path("", include("apps.account.urls.urls_api")),
    path("", include("apps.account.urls.urls_template")),
]