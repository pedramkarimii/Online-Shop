from django.urls import path
from apps.order.views.views_template import views_order_item

"""
This code defines several URL patterns for handling order item operations using class-based views from the
 `views_order_item` module within the `views_template` directory of the `apps.order.views` package.
- The `urlpatterns` list contains four URL patterns.
- Each `path` function call defines a unique URL route and associates it with a specific class-based view.
  - `'add-order-item/<int:pk>/'`: Maps to `views_order_item.AddOrderItemView.as_view()`, allowing users to add an 
  order item. `<int:pk>` captures an integer value and passes it as a keyword argument named `pk` to the view.
  - `'detail-order-item/'`: Maps to `views_order_item.ShowOrderItemProductView.as_view()`, which displays details of 
  order items.
  - `'update-order-item/<int:pk>/'`: Maps to `views_order_item.UpdateOrderItemProductView.as_view()`, allowing users 
  to update an existing order item. `<int:pk>` captures the primary key of the order item to be updated.
  - `'delete-order-item/<int:pk>/'`: Maps to `views_order_item.DeleteOrderItemProductView.as_view()`, allowing users 
  to delete an existing order item. `<int:pk>` captures the primary key of the order item to be deleted.
- Each URL pattern is assigned a unique `name`, which can be used to reference the URL pattern in templates or other 
parts of the Django application.
These patterns provide endpoints for performing CRUD (Create, Read, Update, Delete) operations on order items within 
the web application.
"""
urlpatterns = [
    path('add-order-item/<int:pk>/', views_order_item.AddOrderItemView.as_view(), name='add_order_item'),
    path('detail-order-item/', views_order_item.ShowOrderItemProductView.as_view(),
         name='add_order_item_detail_views'),
    path('update-order-item/<int:pk>/', views_order_item.UpdateOrderItemProductView.as_view(),
         name='update_order_item'),
    path('delete-order-item/<int:pk>/', views_order_item.DeleteOrderItemProductView.as_view(),
         name='delete_order_item'),
]
