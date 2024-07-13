from django.urls import path, include

"""
This code defines URL patterns for a Django project by including URL configurations from different modules related to 
    orders. 
- The first `path` function includes URL patterns for payment-related views from the module
    `apps.order.urls.urls_template.payment`.
- The second `path` function includes URL patterns for order item-related views from the module 
    `apps.order.urls.urls_template.order_item`.
- The third `path` function includes URL patterns for order-related views from the module 
    `apps.order.urls.urls_template.order`.
Each `include` function references another URL configuration, promoting a modular and organized URL structure 
    in the application.
"""

urlpatterns = [
    path("", include("apps.order.urls.urls_template.payment")),
    path("", include("apps.order.urls.urls_template.order_item")),
    path("", include("apps.order.urls.urls_template.order")),
]
