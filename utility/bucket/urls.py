from django.urls import path, re_path
from .bucket_views import BucketView, BucketDeleteObjView, BucketDownloadObjView

"""
This code defines the URL patterns for the bucket-related views in a Django project. 
It maps specific URLs to corresponding class-based views (CBVs) for handling bucket operations such as showing, 
downloading, and deleting objects.

1. `path('showbucket', BucketView.as_view(), name='bucket_main')`:
   - Maps the URL `showbucket` to the `BucketView` class-based view.
   - The name `bucket_main` is used to refer to this URL pattern.

2. `re_path(r'^download_obj_bucket/(?P<key>.+)/$', BucketDownloadObjView.as_view(), name='download_obj_bucket')`:
   - Uses a regular expression to map URLs starting with `download_obj_bucket/` followed by any sequence of characters 
   (captured as `key`) to the `BucketDownloadObjView` class-based view.
   - The name `download_obj_bucket` is used to refer to this URL pattern.

3. `re_path(r'^delete_obj_bucket/(?P<key>.+)/$', BucketDeleteObjView.as_view(), name='deleting_obj_bucket')`:
   - Uses a regular expression to map URLs starting with `delete_obj_bucket/` followed by any sequence of characters 
   (captured as `key`) to the `BucketDeleteObjView` class-based view.
   - The name `deleting_obj_bucket` is used to refer to this URL pattern.

The `re_path` function is used for more complex URL matching using regular expressions, 
allowing for dynamic segments in the URL (e.g., capturing the `key` parameter).
"""
urlpatterns = [
    path('showbucket', BucketView.as_view(), name='bucket_main'),
    re_path(r'^download_obj_bucket/(?P<key>.+)/$', BucketDownloadObjView.as_view(), name='download_obj_bucket'),
    re_path(r'^delete_obj_bucket/(?P<key>.+)/$', BucketDeleteObjView.as_view(), name='deleting_obj_bucket'),
]
