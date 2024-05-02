from django.urls import path
from apps.public.views.views_template import views_home

urlpatterns = [
    path("", views_home.HomeView.as_view(), name="home"),
]
