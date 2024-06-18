from django.urls import path
from apps.order.views.views_template import views_order

urlpatterns = [

    path('add-order/<int:pk>/', views_order.AddOrderView.as_view(), name='add_order'),
]
