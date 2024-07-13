from django.urls import path
from apps.account.views.views_template import views_address

"""
URL configuration for address-related views:
- "address-create/": Maps to AddressCreateView for creating a new address.
- "address-detail/<int:pk>/": Maps to AddressDetailView for viewing an address by its primary key.
- "address-update/<int:pk>/": Maps to AddressUpdateView for updating an address by its primary key.
- "address-delete/<int:pk>/": Maps to AddressDeleteView for deleting an address by its primary key.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
urlpatterns = [
    path("address-create/", views_address.AddressCreateView.as_view(), name="address_create"),
    path("address-detail/<int:pk>/", views_address.AddressDetailView.as_view(), name="address_detail"),
    path("address-update/<int:pk>/", views_address.AddressUpdateView.as_view(), name="address_update"),
    path("address-delete/<int:pk>/", views_address.AddressDeleteView.as_view(), name="address_delete"),
]
