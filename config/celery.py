import os
from celery import Celery
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", base_url="http://localhost")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

log_file = "/var/log/celery.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'
