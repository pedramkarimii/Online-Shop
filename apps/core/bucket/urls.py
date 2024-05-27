from django.urls import path, re_path
from .bucket_views import BucketView, BucketDeleteObjView, BucketDownloadObjView

urlpatterns = [
    path('showbucket', BucketView.as_view(), name='bucket_main'),
    re_path(r'^download_obj_bucket/(?P<key>.+)/$', BucketDownloadObjView.as_view(), name='download_obj_bucket'),
    re_path(r'^delete_obj_bucket/(?P<key>.+)/$', BucketDeleteObjView.as_view(), name='deleting_obj_bucket'),
]
