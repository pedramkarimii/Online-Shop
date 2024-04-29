from django.urls import path, include

urlpatterns = [
    path("", include("apps.public.urls.urls_template.login")),
    path("", include("apps.public.urls.urls_template.home")),
]