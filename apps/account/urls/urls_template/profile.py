from django.urls import path
from apps.account.views.views_template import views_profile

"""
URL configuration for profile-related views:
- "profile-create/": Maps to ProfileCreateView for creating a new profile.
- "profile/<int:pk>/": Maps to ProfileDetailView for viewing a profile by its primary key.
- "profile-delete/<int:pk>/": Maps to ProfileDeleteView for deleting a profile by its primary key.
- "profile-update/<int:pk>/": Maps to ProfileUpdateView for updating a profile by its primary key.
Each view is converted to a callable view function using the `as_view()` method.
The names are used for URL reversing.
"""
urlpatterns = [
    path("profile-create/", views_profile.ProfileCreateView.as_view(), name="profile_create"),
    path("profile/<int:pk>/", views_profile.ProfileDetailView.as_view(), name="profile_detail"),
    path("profile-delete/<int:pk>/", views_profile.ProfileDeleteView.as_view(), name="profile_delete"),
    path("profile-update/<int:pk>/", views_profile.ProfileUpdateView.as_view(), name="profile_update"),
]
