from django.urls import path
from apps.product.views.views_template import views_inventory

"""
Defines Django URL patterns for managing inventory-related operations using views from the `views_inventory` module.
- `path('inventory-create/', views_inventory.InventoryCreateView.as_view(), name='inventory_create')`:
  Maps to a view (`InventoryCreateView`) that handles creating new inventory entries. The URL pattern is named 
  'inventory_create'.
- `path('admin-inventory-list/', views_inventory.AdminInventoryListView.as_view(), name='admin_inventory_list')`:
  Maps to a view (`AdminInventoryListView`) that lists all inventory entries. The URL pattern is named 
  'admin_inventory_list'.
- `path('inventory-detail/<int:pk>/', views_inventory.InventoryDetailView.as_view(), name='inventory_detail')`:
  Maps to a view (`InventoryDetailView`) that shows details of a specific inventory entry identified by `pk`. The URL 
  pattern is named 'inventory_detail'.
- `path('inventory-update/<int:pk>/', views_inventory.InventoryUpdateView.as_view(), name='inventory_update')`:
  Maps to a view (`InventoryUpdateView`) that handles updating an inventory entry identified by `pk`. The URL pattern
   is named 'inventory_update'.
- `path('inventory-delete/<int:pk>/', views_inventory.InventoryDeleteView.as_view(), name='inventory_delete')`:
  Maps to a view (`InventoryDeleteView`) that handles deleting an inventory entry identified by `pk`. The URL pattern
   is named 'inventory_delete'.

Each `path()` function associates a URL endpoint with a corresponding view class (`as_view()` method converts the 
class-based view to a callable view) from the `views_inventory` module, providing CRUD (Create, Read, Update, Delete)
 functionality for inventory management within a Django application.
"""
urlpatterns = [
    path('inventory-create/', views_inventory.InventoryCreateView.as_view(),
         name='inventory_create'),
    path('admin-inventory-list/', views_inventory.AdminInventoryListView.as_view(),
         name='admin_inventory_list'),
    path('inventory-detail/<int:pk>/', views_inventory.InventoryDetailView.as_view(),
         name='inventory_detail'),
    path('inventory-update/<int:pk>/', views_inventory.InventoryUpdateView.as_view(),
         name='inventory_update'),
    path('inventory-delete/<int:pk>/', views_inventory.InventoryDeleteView.as_view(),
         name='inventory_delete'),
]
