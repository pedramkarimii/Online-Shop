from django.urls import path
from apps.product.views.views_template import views_add_to_inventory

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
