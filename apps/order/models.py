from django.db import models
from django.core import validators
from apps.core import mixin
from apps.account.models import User, Address
from apps.order import managers
from django.utils.translation import gettext_lazy as _


class OrderItem(mixin.TimestampsStatusFlagMixin):
    """Model representing an item within an order."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order_items")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="product_order_items")
    warehouse_keeper = models.ForeignKey('core.WarehouseKeeper', on_delete=models.CASCADE,
                                         related_name="warehouse_keeper_order_items")
    total_price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, validators=[validators.MinValueValidator(1)])
    objects = managers.OrderItemManager()

    def __str__(self):
        """Return a string representation of the OrderItem."""
        return f"Order Item: {self.product} - Quantity: {self.quantity}"

    class Meta:
        """Additional metadata about the OrderItem model."""
        ordering = ['-create_time']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        indexes = [
            models.Index(
                fields=['user', 'product', 'warehouse_keeper'], name='order_item')]


class Order(mixin.TimestampsStatusFlagMixin):
    """Model representing an order placed by a user."""

    STATUS_CHOICES = (
        ('paid', _('Paid')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    order_items = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="order_items_order")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new',
                              validators=[validators.RegexValidator(
                                  regex=r'^(new|paid|delivered|cancelled)$', message=_('Invalid status'), )])
    objects = managers.OrderManager()

    def __str__(self):
        """Return a string representation of the Order."""
        return f'{self.user} - {self.status}'

    class Meta:
        """Additional metadata about the Order model."""
        ordering = ['-create_time']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(
                fields=['user', 'order_items'], name='user_order_items')]


class StatusOrder(models.Model):
    """Model representing the status of an order."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_status_order")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_order")

    time_accepted_order = models.DateTimeField(null=True, blank=True)
    accepted_order = models.BooleanField(default=False)

    time_shipped_order = models.DateTimeField(null=True, blank=True)
    shipped_order = models.BooleanField(default=False)

    time_deliver_order = models.DateTimeField(null=True, blank=True)
    deliver_order = models.BooleanField(default=False)

    time_rejected_order = models.DateTimeField(null=True, blank=True)
    rejected_order = models.BooleanField(default=False)

    time_cancelled_order = models.DateTimeField(null=True, blank=True)
    cancelled_order = models.BooleanField(default=False)

    deliver = models.BooleanField(default=False)

    objects = managers.StatusOrderManager()

    def __str__(self):
        """Return a string representation of the StatusOrder."""
        return f'{self.order} - {self.deliver}'

    class Meta:
        """Additional metadata about the StatusOrder model."""
        verbose_name = 'Status Order'
        verbose_name_plural = 'Status Orders'
        ordering = ['-time_accepted_order']
        indexes = [
            models.Index(
                fields=['order', 'time_accepted_order'], name='order_time_accepted_order_idx')]
