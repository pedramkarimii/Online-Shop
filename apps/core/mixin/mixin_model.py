from django.db import models
from django.utils import timezone
import random
from enum import Enum


class TimestampsStatusFlagMixin(models.Model):
    """
    A mixin to add timestamp and status flag fields to a model.
    """

    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    update_time = models.DateTimeField(auto_now=True, editable=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


def generate_transaction_id():
    """
    Function to generate a unique transaction ID.
    """
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
    random_part = ''.join(random.choices('0123456789', k=6))
    unique_id = f'{timestamp}{random_part}'
    return unique_id


class PaymentStatusMixin(Enum):
    """
    Enum representing payment status options.
    """

    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
