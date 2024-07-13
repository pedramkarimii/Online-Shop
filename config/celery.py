import os
from celery import Celery
import logging

# Set the Django settings module for the Celery app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Create a Celery instance named "app" with base URL "http://localhost"
app = Celery("config", base_url="http://localhost")

# Configure Celery using Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks defined in the Django app
app.autodiscover_tasks()

# Set up logging to a file specified by log_file
log_file = "/var/log/celery.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# Configure Celery to use Redis as the broker and result backend
app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'
