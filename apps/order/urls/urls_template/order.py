from django.urls import path
from apps.order.views.views_template import views_order

"""
This code defines a URL pattern for the `AddOrderView` in the `views_order` module, located within the `views_template` directory of the `apps.order.views` package.
- The `urlpatterns` list contains a single URL pattern.
- The `path` function defines a URL route for adding an order.
  - `'add-order/<int:pk>/'` is the URL pattern, where `<int:pk>` captures an integer value and passes it as a keyword argument named `pk` to the view.
  - `views_order.AddOrderView.as_view()` references the `AddOrderView` class-based view from the `views_order` module.
  - `name='add_order'` assigns a name to this URL pattern, allowing it to be referenced elsewhere in the code using this name.
This setup allows users to add an order by navigating to the URL that matches the pattern `add-order/<int:pk>/`, where `<int:pk>` is the primary key of the order to be added.
"""

urlpatterns = [
    path('add-order/<int:pk>/', views_order.AddOrderView.as_view(), name='add_order'),
]
