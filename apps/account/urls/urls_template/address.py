from django.urls import path
from apps.account.views.views_template import views_address

urlpatterns = [
    path("address-create/", views_address.AddressCreateView.as_view(), name="address_create"),
    # path("address-detail/<int:pk>/", views_template.AddressDetailView.as_view(), name="address_detail"),
    path("address-update/<int:pk>/", views_address.AddressUpdateView.as_view(), name="address_update"),
    path("address-delete/<int:pk>/", views_address.AddressDeleteView.as_view(), name="address_delete"),
]
