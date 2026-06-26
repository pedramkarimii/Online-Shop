import os
from urllib.parse import quote

from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")

rabbitmq_user = quote(config("RABBITMQ_USER"), safe="")
rabbitmq_password = quote(config("RABBITMQ_PASSWORD"), safe="")
rabbitmq_host = config("RABBITMQ_HOST", default="rabbitmq")
rabbitmq_port = config("RABBITMQ_PORT", cast=int, default=5672)

app.conf.broker_url = (
    f"amqp://{rabbitmq_user}:{rabbitmq_password}"
    f"@{rabbitmq_host}:{rabbitmq_port}//"
)

app.conf.result_backend = config(
    "CELERY_RESULT_BACKEND",
    default="redis://redis:6379/0",
)

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
