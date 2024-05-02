from django.urls import path
from django.views.generic import TemplateView

from apps.public.views.views_template import views_home

urlpatterns = [
    # path("", views_home.HomeView.as_view(), name="home"),
    # path("product/", TemplateView.as_view(template_name='product/product/product.html'), name="product"),
    # path("category/", TemplateView.as_view(template_name='category/categories.html'), name="category"),
]