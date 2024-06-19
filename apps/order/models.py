from django.db import models
from apps.core import validators
from apps.core.mixin import mixin_model
from apps.account.models import User, Address
from apps.order import managers
from django.utils.translation import gettext_lazy as _


class OrderItem(mixin_model.TimestampsStatusFlagMixin):
    """Model representing an item within an order."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order_items")
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="product_order_items")
    # order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="order_order_items")
    total_price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1, validators=[validators.QuantityValidators()],
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


class Order(mixin_model.TimestampsStatusFlagMixin):
    """Model representing an order placed by a user."""
    order_item = models.ManyToManyField(OrderItem, related_name="order_items", verbose_name=_('Order Items'))
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="address_order")
    status = models.CharField(max_length=20, choices=validators.StatusChoice.CHOICES,
                              validators=[validators.StatusValidator()],
                              verbose_name=_('Status'))
    transaction_id = models.CharField(max_length=36, default=mixin_model.generate_transaction_id, unique=True,
                                      verbose_name=_('Transaction'))
    payment_method = models.CharField(max_length=20, choices=validators.PaymentMethodChoice.CHOICES)
    code_discount = models.CharField(max_length=100, validators=[validators.CodeValidator()],
                                     verbose_name=_('Code Discount'), null=True, blank=True)
    finally_price = models.IntegerField(default=0, validators=[validators.FinallyPriceValidator()])

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
        return f' {self.transaction_id} - {self.payment_method} - {self.finally_price} '

    class Meta:
        """Additional metadata about the Order model."""
        ordering = ['-create_time']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(
                fields=['address'], name='user_order_items')]


class OrderPayment(models.Model):
    """Model representing a payment associated with an order."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_payments")
    amount = models.SmallIntegerField(default=0, validators=[validators.AmountValidator()],
                                      verbose_name=_('Amount'))
    cardholder_name = models.CharField(max_length=100, validators=[validators.NameValidator()],
                                       verbose_name=_('Cardholder Name'))
    card_number = models.CharField(max_length=12, validators=[validators.CardNumberValidator()],
                                   verbose_name=_('Card Number'))
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4, validators=[validators.CVVValidator()],
                           verbose_name=_('CVV'))

    status = models.CharField(max_length=20, verbose_name=_('Status'))
    transaction_payment = models.CharField(max_length=36,  unique=True,
                                           default=mixin_model.generate_transaction_id,
                                           verbose_name=_('Transaction Payment'))
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
