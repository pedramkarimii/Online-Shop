from django.db import models
from django.core import validators
from apps.core import mixin
from apps.core.mixin import PaymentStatusMixin, generate_transaction_id
from apps.core import managers
from apps.account.models import User
from apps.order.models import Order
from django.utils.translation import gettext_lazy as _
from apps.product.models import Brand, Product, Category


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
    card_number = models.CharField(max_length=16, validators=[
        validators.RegexValidator(r'^\d{16}$', _('Enter a valid 16-digit card number.'))])
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


class CodeDiscount(mixin.TimestampsStatusFlagMixin):
    """Model representing a discount code associated with a product or category."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_code_discounts')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_code_discounts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_code_discounts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_code_discounts')
    code = models.CharField(max_length=100)
    percentage_discount = models.IntegerField(null=True, blank=True,
                                              validators=[validators.MinValueValidator(0)])
    numerical_discount = models.IntegerField(null=True, blank=True,
                                             validators=[validators.MinValueValidator(0)])
    expiration_date = models.DateTimeField(null=True, blank=True, editable=False)
    is_use = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    objects = managers.CodeDiscountManager()
    soft_delete = managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the CodeDiscount."""
        return f'{self.code} - {self.percentage_discount} - {self.numerical_discount}'

    class Meta:
        """Additional metadata about the CodeDiscount model."""
        ordering = ['-code']
        verbose_name = 'Code Discount'
        verbose_name_plural = 'Code Discounts'
        constraints = [
            models.UniqueConstraint(fields=['code'], name='unique_code')
        ]
        indexes = [
            models.Index(fields=['code']),
        ]


class WarehouseKeeper(mixin.TimestampsStatusFlagMixin):
    """Model representing a user responsible for managing inventory in a warehouse."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_warehouse_keepers')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_warehouse_keepers')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_warehouse_keepers')
    quantity = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)

    objects = managers.WarehouseKeeperManager()
    soft_delete = managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the WarehouseKeeper."""
        return f'{self.user.name} - {self.product.name} - {self.quantity}'

    class Meta:
        """Additional metadata about the WarehouseKeeper model."""
        ordering = ['-user', '-product']
        verbose_name = 'Warehouse Keeper'
        verbose_name_plural = 'Warehouse Keepers'
        indexes = [
            models.Index(fields=['user', 'product']),
        ]
