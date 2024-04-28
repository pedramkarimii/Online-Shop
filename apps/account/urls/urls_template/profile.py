from django.urls import path
from apps.account.views.views_template import views_profile

urlpatterns = [
    path("profile-create/", views_profile.ProfileCreateView.as_view(), name="profile_create"),
    path("profile/<int:pk>/", views_profile.ProfileDetailView.as_view(), name="profile_detail"),
    path("profile-delete/<int:pk>/", views_profile.ProfileDeleteView.as_view(), name="profile_delete"),
    path("profile-update/<int:pk>/", views_profile.ProfileUpdateView.as_view(), name="profile_update"),
]
