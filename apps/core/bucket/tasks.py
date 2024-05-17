from .bucket import buckets
from celery import shared_task


def all_buckets_objects_task():
    result = buckets.get_object()
    return result


@shared_task
def delete_object_task(key):
    result = buckets.delete_object(key)
    return result


@shared_task
def download_object_task(key):
    result = buckets.download_object(key)
    return result
