import boto3
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Bucket:
    def __init__(self):
        session = boto3.session.Session()
        self.connection_s3_client = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )

    def get_object(self):
        result = self.connection_s3_client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None

    def delete_object(self, key):
        self.connection_s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        try:
            self.connection_s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            return True
        except Exception as e:
            logging.error(f"Error deleting object from bucket: {e}")
            return False

    def download_object(self, key):
        local_file_path = settings.AWS_LOCAL_STORAGE + key
        try:
            with open(local_file_path, 'wb') as f:
                self.connection_s3_client.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)
            logger.info(f"Downloaded object '{key}' to '{local_file_path}'")
            return local_file_path
        except Exception as e:
            logger.error(f"Error downloading object '{key}': {e}")
            return None


buckets = Bucket()
