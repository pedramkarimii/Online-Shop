from django.urls import path
from apps.product.views.views_template import views_add_to_inventory

"""
Defines Django URL patterns for managing inventory-related operations using views from the 
`views_add_to_inventory` module.
- `path('add-to-inventory-create/', views_add_to_inventory.AddToInventoryCreateView.as_view(),
 name='warehouse_keeper_create')`:
  Maps to a view (`AddToInventoryCreateView`) that handles creating new inventory entries. The URL pattern is named 
  'warehouse_keeper_create'.
- `path('admin-add-to-inventory-list/', views_add_to_inventory.AdminAddToInventoryListView.as_view(),
 name='admin_warehouse_keeper_list')`:
  Maps to a view (`AdminAddToInventoryListView`) that lists all inventory entries. The URL pattern is named 
  'admin_warehouse_keeper_list'.
- `path('add-to-inventory-detail/<int:pk>/', views_add_to_inventory.AddToInventoryDetailView.as_view(), 
name='warehouse_keeper_detail')`:
  Maps to a view (`AddToInventoryDetailView`) that shows details of a specific inventory entry identified 
  by `pk`. The URL pattern is named 'warehouse_keeper_detail'.
- `path('add-to-inventory-update/<int:pk>/', views_add_to_inventory.AddToInventoryUpdateView.as_view(),
 name='warehouse_keeper_update')`:
  Maps to a view (`AddToInventoryUpdateView`) that handles updating an inventory entry identified by `pk`. 
  The URL pattern is named 'warehouse_keeper_update'.
- `path('add-to-inventory-delete/<int:pk>/', views_add_to_inventory.AddToInventoryDeleteView.as_view(),
 name='warehouse_keeper_delete')`:
  Maps to a view (`AddToInventoryDeleteView`) that handles deleting an inventory entry identified by `pk`. 
  The URL pattern is named 'warehouse_keeper_delete'.
Each `path()` function associates a URL pattern with a corresponding view class (`as_view()` method converts
 the class-based view to a callable view) from the `views_add_to_inventory` module, providing CRUD (Create, Read, 
 Update, Delete) functionality for inventory management within a Django application.
"""
urlpatterns = [
    path('add-to-inventory-create/', views_add_to_inventory.AddToInventoryCreateView.as_view(),
         name='warehouse_keeper_create'),
    path('admin-add-to-inventory-list/', views_add_to_inventory.AdminAddToInventoryListView.as_view(),
         name='admin_warehouse_keeper_list'),
    path('add-to-inventory-detail/<int:pk>/', views_add_to_inventory.AddToInventoryDetailView.as_view(),
         name='warehouse_keeper_detail'),
    path('add-to-inventory-update/<int:pk>/', views_add_to_inventory.AddToInventoryUpdateView.as_view(),
         name='warehouse_keeper_update'),
    path('add-to-inventory-delete/<int:pk>/', views_add_to_inventory.AddToInventoryDeleteView.as_view(),
         name='warehouse_keeper_delete'),
]
