from django.urls import path
from apps.order.views.views_template import views_order_item

urlpatterns = [

    path('add-order-item/<int:pk>/', views_order_item.AddOrderItemView.as_view(), name='add_order_item'),
    path('detail-order-item/', views_order_item.ShowOrderItemProductView.as_view(),
         name='add_order_item_detail_views'),
    path('update-order-item/<int:pk>/', views_order_item.UpdateOrderItemProductView.as_view(),
         name='update_order_item'),
    path('delete-order-item/<int:pk>/', views_order_item.DeleteOrderItemProductView.as_view(),
         name='delete_order_item'),
]
