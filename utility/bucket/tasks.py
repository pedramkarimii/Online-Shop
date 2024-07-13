from .bucket import buckets
from celery import shared_task


@shared_task
def all_buckets_objects_task():
    """
    Task to retrieve all objects from a bucket.

    Returns:
        The result of the get_object method from the buckets module.
    """
    result = buckets.get_object()
    return result


@shared_task
def delete_object_task(key):
    """
    Task to delete an object from a bucket.

    Args:
        key (str): The key (path) of the object to be deleted.

    Returns:
        The result of the delete_object method from the buckets module.
    """
    return buckets.delete_object(key)


@shared_task
def download_object_task(key):
    """
    Task to download an object from a bucket.

    Args:
        key (str): The key (path) of the object to be downloaded.

    Returns:
        The result of the download_object method from the buckets module.
    """
    return buckets.download_object(key)
