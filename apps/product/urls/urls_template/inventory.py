from django.urls import path
from apps.product.views.views_template import views_inventory

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
