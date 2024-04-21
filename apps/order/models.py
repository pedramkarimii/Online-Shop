from django.db import models
from django.core import validators
from apps.core import mixin
from apps.account.models import User, Address, CodeDiscount
from apps.order import managers
from django.utils.translation import gettext_lazy as _


class OrderItem(mixin.TimestampsStatusFlagMixin):
    """Model representing an item within an order."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_order_items")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="product_order_items")
    total_price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, validators=[validators.MinValueValidator(1)],
                                           verbose_name=_('Quantity'))
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
    payment_method_choices = [
        ('credit_card', _('Credit Card')),
        ('debit_card', _('Debit Card')),
        ('paypal', _('PayPal')),
        ('bank_transfer', _('Bank Transfer')),
        ('cash', _('Cash')),
    ]

    STATUS_CHOICES = (
        ('paid', _('Paid')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    order_items = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="order_items_order")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address_order")
    code_discount = models.ForeignKey(CodeDiscount, on_delete=models.CASCADE, related_name="code_discount_order",
                                      null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              validators=[validators.RegexValidator(
                                  regex=r'^(paid|delivered|cancelled)$', message=_('Invalid status'), )],
                              verbose_name=_('Status'))
    transaction_id = models.CharField(max_length=36, default=mixin.generate_transaction_id, unique=True,
                                      verbose_name=_('Transaction'))
    payment_method = models.CharField(max_length=20, choices=payment_method_choices)
    finally_price = models.IntegerField(default=0, validators=[validators.MinValueValidator(0)])

    time_accepted_order = models.DateTimeField(null=True, blank=True, verbose_name=_('Time Accepted Order'))
    accepted_order = models.BooleanField(default=False)

    time_shipped_order = models.DateTimeField(null=True, blank=True, verbose_name=_('Time Shipped Order'))
    shipped_order = models.BooleanField(default=False)

    time_deliver_order = models.DateTimeField(null=True, blank=True, verbose_name=_('Time Deliver Order'))
    deliver_order = models.BooleanField(default=False)

    time_rejected_order = models.DateTimeField(null=True, blank=True, verbose_name=_('Time Rejected Order'))
    rejected_order = models.BooleanField(default=False)

    time_cancelled_order = models.DateTimeField(null=True, blank=True, verbose_name=_('Time Cancelled Order'))
    cancelled_order = models.BooleanField(default=False)
    objects = managers.OrderManager()

    def __str__(self):
        """Return a string representation of the Order."""
        return f'{self.order_items} - {self.address} - {self.status}'

    class Meta:
        """Additional metadata about the Order model."""
        ordering = ['-create_time']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(
                fields=['order_items'], name='user_order_items')]


class OrderPayment(models.Model):
    """Model representing a payment associated with an order."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_payments")
    amount = models.SmallIntegerField(default=0, validators=[validators.MinValueValidator(0)],
                                      verbose_name=_('Amount'))
    cardholder_name = models.CharField(max_length=100, validators=[validators.MinLengthValidator(3)],
                                       verbose_name=_('Cardholder Name'))
    card_number = models.CharField(max_length=12, validators=[
        validators.RegexValidator(r'^\d{12}$', _('Enter a valid 12-digit card number.'))],
                                   verbose_name=_('Card Number'))
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4, validators=[
        validators.RegexValidator(r'^\d{3,4}$', _('Enter a valid 3 or 4-digit CVV.'))],
                           verbose_name=_('CVV'))

    status = models.CharField(max_length=20,
                              choices=[(status.value, status.name.capitalize()) for status in mixin.PaymentStatusMixin],
                              default=mixin.PaymentStatusMixin.PENDING.value, verbose_name=_('Status'))
    payment_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Payment Time'))
    is_paid = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    objects = managers.OrderPaymentManager()

    def __str__(self):
        """Return a string representation of the OrderPayment."""
        return f'Transaction ID: {self.order}, Amount: {self.amount}, Status: {self.status}'

    class Meta:
        """Additional metadata about the OrderPayment model."""
        ordering = ['-payment_time']
        verbose_name = 'Order Payment'
        verbose_name_plural = 'Order Payments'
        indexes = [
            models.Index(fields=['payment_time', 'order']),
        ]
