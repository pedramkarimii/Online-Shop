from django.urls import path
from apps.product.views.views_template import views_discount_create

"""
Defines Django URL patterns for managing discount-related operations using views from the `views_discount_create` module.
- `path('discount-create/', views_discount_create.DiscountCreateView.as_view(), name='discount_create')`:
  Maps to a view (`DiscountCreateView`) that handles creating new discount entries. The URL pattern is named 
  'discount_create'.
- `path('admin-discount-list/', views_discount_create.AdminDiscountListView.as_view(), name='admin_discount_list')`:
  Maps to a view (`AdminDiscountListView`) that lists all discount entries. The URL pattern is named 
  'admin_discount_list'.
- `path('discount-detail/<int:pk>/', views_discount_create.DiscountDetailView.as_view(), name='discount_detail')`:
  Maps to a view (`DiscountDetailView`) that shows details of a specific discount entry identified by `pk`.
   The URL pattern is named 'discount_detail'.
- `path('discount-update/<int:pk>/', views_discount_create.DiscountUpdateView.as_view(), name='discount_update')`:
  Maps to a view (`DiscountUpdateView`) that handles updating a discount entry identified by `pk`. The URL pattern
   is named 'discount_update'.
- `path('discount-delete/<int:pk>/', views_discount_create.DiscountDeleteView.as_view(), name='discount_delete')`:
  Maps to a view (`DiscountDeleteView`) that handles deleting a discount entry identified by `pk`. The URL pattern
   is named 'discount_delete'.
Each `path()` function associates a URL endpoint with a corresponding view class (`as_view()` method converts the
 class-based view to a callable view) from the `views_discount_create` module, providing CRUD (Create, Read,
  Update, Delete) functionality for discount management within a Django application.
"""
urlpatterns = [
    path('discount-create/', views_discount_create.DiscountCreateView.as_view(), name='discount_create'),
    path('admin-discount-list/', views_discount_create.AdminDiscountListView.as_view(), name='admin_discount_list'),
    path('discount-detail/<int:pk>/', views_discount_create.DiscountDetailView.as_view(), name='discount_detail'),
    path('discount-update/<int:pk>/', views_discount_create.DiscountUpdateView.as_view(), name='discount_update'),
    path('discount-delete/<int:pk>/', views_discount_create.DiscountDeleteView.as_view(), name='discount_delete'),
]
