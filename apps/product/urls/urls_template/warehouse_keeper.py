from django.urls import path
from apps.product.views.views_template import views_warehouse_keeper

urlpatterns = [
    path('warehouse-keeper-create/', views_warehouse_keeper.WarehouseKeeperCreateView.as_view(),
         name='warehouse_keeper_create'),
    path('admin-warehouse-keeper-list/', views_warehouse_keeper.AdminWarehouseKeeperListView.as_view(),
         name='admin_warehouse_keeper_list'),
    path('warehouse-keeper-detail/<int:pk>/', views_warehouse_keeper.WarehouseKeeperDetailView.as_view(),
         name='warehouse_keeper_detail'),
    path('warehouse-keeper-update/<int:pk>/', views_warehouse_keeper.WarehouseKeeperUpdateView.as_view(),
         name='warehouse_keeper_update'),
    path('warehouse-keeper-delete/<int:pk>/', views_warehouse_keeper.WarehouseKeeperDeleteView.as_view(),
         name='warehouse_keeper_delete'),
]
