import os
from datetime import datetime
import boto3
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Bucket:
    """
    Class for interacting with an S3 bucket.
    """
    def __init__(self):
        """
        Initialize the S3 client using the provided AWS credentials and endpoint URL.
        """
        session = boto3.session.Session()
        self.connection_s3_client = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )

    def get_object(self):
        """
        Retrieve a list of objects from the S3 bucket.
        Returns:
            list: A list of object dictionaries, or None if the bucket is empty.
        """
        result = self.connection_s3_client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None

    def delete_object(self, key):
        """
        Delete an object from the S3 bucket and also delete the corresponding local file.
        Args:
            key (str): The key (path) of the object to be deleted.
        Returns:
            bool: True if the object was successfully deleted, False otherwise.
        """
        try:
            # Delete object from S3 bucket
            self.connection_s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            logger.info(f"Deleted object '{key}' from bucket '{settings.AWS_STORAGE_BUCKET_NAME}'")

            local_file_path = settings.AWS_LOCAL_STORAGE + key
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
                logger.info(f"Deleted local file '{local_file_path}'")

            return True
        except Exception as e:
            logger.error(f"Error deleting object '{key}' from bucket '{settings.AWS_STORAGE_BUCKET_NAME}': {e}")
            return False

    def download_object(self, key):
        """
        Download an object from the S3 bucket to a local file.
        Args:
            key (str): The key (path) of the object to be downloaded.
        Returns:
            str: The local file path where the object was downloaded, or None if an error occurred.
        Notes:
            The local file path is constructed based on the AWS_LOCAL_STORAGE setting and the current year and month.
            For example, if AWS_LOCAL_STORAGE is '/path/to/uploads/%Y/%m/', the local file path will be
            '/path/to/uploads/2023/05/object_name.ext'
        """
        local_file_path = settings.AWS_LOCAL_STORAGE + key
        local_file_path = local_file_path.replace('%Y', str(datetime.now().year))
        local_file_path = local_file_path.replace('%m', str(datetime.now().month))
        local_dir_path = os.path.dirname(local_file_path)
        os.makedirs(local_dir_path, exist_ok=True)  # Create directories if they don't exist
        try:
            with open(local_file_path, 'wb') as f:
                self.connection_s3_client.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)
            logger.info(f"Downloaded object '{key}' to '{local_file_path}'")
            return local_file_path
        except Exception as e:
            logger.error(f"Error downloading object '{key}': {e}")
            return None


buckets = Bucket()
