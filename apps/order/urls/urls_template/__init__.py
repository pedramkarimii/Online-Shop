from django.urls import path, include

urlpatterns = [
    path("", include("apps.order.urls.urls_template.payment")),
    path("", include("apps.order.urls.urls_template.order_item")),
    path("", include("apps.order.urls.urls_template.order")),
]
