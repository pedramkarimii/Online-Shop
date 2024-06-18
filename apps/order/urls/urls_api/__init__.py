from django.urls import path, include

urlpatterns = [
    path("", include("apps.order.urls.urls_api.checkout")),
    path("", include("apps.order.urls.urls_api.order_item")),
]
