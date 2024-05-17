from django.urls import path, include
from .bucket_views import BucketView, BucketDeleteObjView, BucketDownloadObjView

urlpatterns = [
    path('', BucketView.as_view(), name='bucket_main'),
    path('delete_obj_bucket/<str:key>/', BucketDeleteObjView.as_view(), name='deleting_obj_bucket'),
    path('download_obj_bucket/<str:key>/', BucketDownloadObjView.as_view(), name='download_obj_bucket'),
]