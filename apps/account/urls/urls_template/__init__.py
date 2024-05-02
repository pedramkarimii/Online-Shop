from django.urls import path, include

urlpatterns = [
    path("", include("apps.account.urls.urls_template.address")),
    path("", include("apps.account.urls.urls_template.role")),
    path("", include("apps.account.urls.urls_template.auth")),
    path("", include("apps.account.urls.urls_template.user")),
    path("", include("apps.account.urls.urls_template.discount_cod")),
    path("", include("apps.account.urls.urls_template.profile")),
    path("", include("apps.account.urls.urls_template.resat_password")),
]