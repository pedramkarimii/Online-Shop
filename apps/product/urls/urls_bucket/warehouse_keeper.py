from django.urls import path
from apps.product.views import views_template

urlpatterns = [
    # path('warehouse-keeper-create/', views_template.WarehouseKeeperCreateView.as_view(),
    #      name='warehouse_keeper_create'),
    # # path('warehouse-keeper-detail/<int:pk>/', views_template.WarehouseKeeperDetailView.as_view(), name='warehouse_keeper_detail'),
    # path('warehouse-keeper-update/<int:pk>/', views_template.WarehouseKeeperUpdateView.as_view(),
    #      name='warehouse_keeper_update'),
    # path('warehouse-keeper-delete/<int:pk>/', views_template.WarehouseKeeperDeleteView.as_view(),
    #      name='warehouse_keeper_delete'),
]
