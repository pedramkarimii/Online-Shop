from django.db import models
from django.core import validators
from apps.core import mixin
from apps.account.models import User, Address
from apps.core.mixin import PaymentStatusMixin, generate_transaction_id
from apps.order import managers
from django.utils.translation import gettext_lazy as _


class OrderItem(mixin.TimestampsStatusFlagMixin):
    """Model representing an item within an order."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order_items")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="product_order_items")
    total_price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, validators=[validators.MinValueValidator(1)])
    objects = managers.OrderItemManager()

    def __str__(self):
        """Return a string representation of the OrderItem."""
        return f"Order Item: {self.product} - Quantity: {self.quantity}"

    class Meta:
        """Additional metadata about the OrderItem model."""
        ordering = ('-create_time',)
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        indexes = [
            models.Index(
                fields=('user', 'product'), name='order_item')]


class Order(mixin.TimestampsStatusFlagMixin):
    """Model representing an order placed by a user."""

    STATUS_CHOICES = (
        ('paid', _('Paid')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_orders")
    order_items = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="order_items_order")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address_order")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
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


class OrderPayment(models.Model):
    """Model representing a payment associated with an order."""

    payment_method_choices = [
        ('credit_card', _('Credit Card')),
        ('debit_card', _('Debit Card')),
        ('paypal', _('PayPal')),
        ('bank_transfer', _('Bank Transfer')),
        ('cash', _('Cash')),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_payments")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validators.MinValueValidator(0)])
    cardholder_name = models.CharField(max_length=100, validators=[validators.MinLengthValidator(3)])
    card_number = models.CharField(max_length=12, validators=[
        validators.RegexValidator(r'^\d{12}$', _('Enter a valid 12-digit card number.'))])
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4, validators=[
        validators.RegexValidator(r'^\d{3,4}$', _('Enter a valid 3 or 4-digit CVV.'))])
    transaction_id = models.CharField(max_length=36, default=generate_transaction_id, unique=True)
    payment_method = models.CharField(max_length=20, choices=payment_method_choices)
    status = models.CharField(max_length=20,
                              choices=[(status.value, status.name.capitalize()) for status in PaymentStatusMixin],
                              default=PaymentStatusMixin.PENDING.value)
    payment_time = models.DateTimeField(auto_now_add=True, editable=False)
    is_paid = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    objects = managers.OrderPaymentManager()

    def __str__(self):
        """Return a string representation of the OrderPayment."""
        return f'Transaction ID: {self.transaction_id}, Amount: {self.amount}, Status: {self.status}'

    class Meta:
        """Additional metadata about the OrderPayment model."""
        ordering = ['-payment_time']
        verbose_name = 'Order Payment'
        verbose_name_plural = 'Order Payments'
        indexes = [
            models.Index(fields=['payment_time', 'user', 'order']),
        ]


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

    objects = managers.StatusOrderManager()

    def __str__(self):
        """Return a string representation of the StatusOrder."""
        return f'{self.order} - {self.deliver_order}'

    class Meta:
        """Additional metadata about the StatusOrder model."""
        verbose_name = 'Status Order'
        verbose_name_plural = 'Status Orders'
        ordering = ['-time_accepted_order']
        indexes = [
            models.Index(
                fields=['order', 'time_accepted_order'], name='order_time_accepted_order_idx')]
