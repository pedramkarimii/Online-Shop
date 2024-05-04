from django.urls import path, include

urlpatterns = [
    path("", include("apps.product.urls.urls_template.product")),
    path("", include("apps.product.urls.urls_template.comment")),
    path("", include("apps.product.urls.urls_template.category")),
    path("", include("apps.product.urls.urls_template.brand")),
    path("", include("apps.product.urls.urls_template.discount")),
    path("", include("apps.product.urls.urls_template.add_to_inventory")),
    path("", include("apps.product.urls.urls_template.inventory")),
]
