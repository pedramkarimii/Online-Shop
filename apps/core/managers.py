from django.db import models
from django.db.models import Sum
import pytz
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet for handling soft deletes."""

    def delete(self):
        """Soft delete queryset items."""
        return super().update(is_deleted=True, is_active=False)

    def undelete(self):
        """Undelete previously soft-deleted items."""
        return super().update(is_deleted=False, is_active=True)

    def activate(self):
        """Activate queryset items."""
        return super().update(is_active=True)

    def deactivate(self):
        """Deactivate queryset items."""
        return super().update(is_active=False)

    def archive(self):
        """Retrieve all items."""
        return super().all()


class DeleteManager(models.Manager):
    """Manager for handling soft deletes."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = SoftDeleteQuerySet(self.model)
        return self.__queryset

    def delete(self):
        """Soft delete items."""
        return self.get_queryset().delete()

    def undelete(self):
        """Undelete items."""
        return self.get_queryset().undelete()

    def activate(self):
        """Activate items."""
        return self.get_queryset().activate()

    def deactivate(self):
        """Deactivate items."""
        return self.get_queryset().deactivate()

    def archive(self):
        """Retrieve all items."""
        return self.get_queryset().archive()


class CodeDiscountQuerySet(models.QuerySet):
    """QuerySet for handling code discounts."""

    def get_discount(self, code):
        """Retrieve a discount by its code."""
        return self.get(code=code)

    def is_valid(self):
        """Check if the discount code is currently valid."""
        now = timezone.now()
        return self.filter(
            is_expired=False,
            expiration_date__gte=now
        )

    def active_and_valid_discounts(self):
        """Retrieve active and currently valid discounts."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(is_active=True, expiration_date__gte=now)

    def valid_discounts(self):
        """Retrieve currently valid discounts."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(is_active=True, expiration_date__gte=now, is_expired=False)

    def expired_discounts(self):
        """Retrieve expired discounts."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(expiration_date__lt=now)

    def get_discount_by_code_and_user(self, code, user):
        """Retrieve a discount by its code and associated user."""
        now = timezone.now().astimezone(pytz.timezone('Asia/Tehran'))
        return self.filter(code=code, user=user, expiration_date__gte=now).first()


class CodeDiscountManager(models.Manager):
    """Manager for handling code discounts."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = CodeDiscountQuerySet(self.model)
        return self.__queryset

    def get_discount(self, code):
        """Retrieve a discount by its code."""
        return self.get_queryset().get_discount(code)

    def is_valid(self):
        """Check if a discount is valid."""
        return self.get_queryset().is_valid()

    def get_discounts(self, codes):
        """Retrieve discounts by a list of codes."""
        return self.get_queryset().filter(code__in=codes)

    def active_discounts(self):
        """Retrieve active discounts."""
        return self.get_queryset().filter(is_active=True)

    def inactive_discounts(self):
        """Retrieve inactive discounts."""
        return self.get_queryset().filter(is_active=False)

    def expired_discounts(self):
        """Retrieve expired discounts."""
        return self.get_queryset().expired_discounts()

    def active_and_valid_discounts(self):
        """Retrieve active and valid discounts."""
        return self.get_queryset().active_and_valid_discounts()

    def valid_discounts(self):
        """Retrieve valid discounts."""
        return self.get_queryset().valid_discounts()

    def get_discount_by_code_and_user(self, code, user):
        """Retrieve a discount by its code and associated user."""
        return self.get_queryset().get_discount_by_code_and_user(code, user)


class OrderPaymentQuerySet(models.QuerySet):
    def total_payment_amount(self):
        """
        Calculate the total amount of all payments.
        """
        return self.aggregate(total_payment_amount=Sum('amount'))['total_payment_amount'] or 0

    def successful_payments(self):
        """
        Get all successful payments.
        """
        return self.filter(is_paid=True, is_cancelled=False, is_failed=False)

    def failed_payments(self):
        """
        Get all failed payments.
        """
        return self.filter(is_failed=True)

    def pending_payments(self):
        """
        Get all pending payments.
        """
        return self.filter(is_paid=False, is_cancelled=False, is_failed=False)

    def total_successful_payments(self):
        """
        Count the number of successful payments.
        """
        return self.successful_payments().count()

    def total_failed_payments(self):
        """
        Count the number of failed payments.
        """
        return self.failed_payments().count()

    def total_pending_payments(self):
        """
        Count the number of pending payments.
        """
        return self.pending_payments().count()


class OrderPaymentManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = OrderPaymentQuerySet(self.model)
        return self.__queryset

    def total_payment_amount(self):
        """
        Calculate the total amount of all payments.
        """
        return self.get_queryset().total_payment_amount()

    def successful_payments(self):
        """
        Get all successful payments.
        """
        return self.get_queryset().successful_payments()

    def failed_payments(self):
        """
        Get all failed payments.
        """
        return self.get_queryset().failed_payments()

    def pending_payments(self):
        """
        Get all pending payments.
        """
        return self.get_queryset().pending_payments()

    def total_successful_payments(self):
        """
        Count the number of successful payments.
        """
        return self.get_queryset().total_successful_payments()

    def total_failed_payments(self):
        """
        Count the number of failed payments.
        """
        return self.get_queryset().total_failed_payments()

    def total_pending_payments(self):
        """
        Count the number of pending payments.
        """
        return self.get_queryset().total_pending_payments()


class WarehouseKeeperQuerySet(models.QuerySet):
    def available_products(self):
        """
        Returns warehouse keepers with available products.
        """
        return self.filter(quantity__gt=0)

    def by_brand(self, brand_id):
        """
        Returns warehouse keepers by a specific brand.
        """
        return self.filter(brand_id=brand_id)

    def active_products(self):
        """
        Returns warehouse keepers with active products.
        """
        return self.filter(product__is_active=True)

    def not_active_products(self):
        """
        Returns warehouse keepers with inactive products.
        """
        return self.filter(product__is_active=False)

    def delete_products(self):
        """
        Deletes warehouse keepers with zero quantity products.
        """
        return self.filter(quantity=0).delete()

    def total_quantity_lower_than(self, value):
        """
        Returns warehouse keepers with a total quantity lower than the specified value.
        """
        return self.annotate(total_quantity=Sum('quantity')).filter(total_quantity__lt=value)


class WarehouseKeeperManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = WarehouseKeeperQuerySet(self.model)
        return self.__queryset

    def available_products(self):
        """
        Returns warehouse keepers with available products using the custom queryset.
        """
        return self.get_queryset().available_products()

    def by_brand(self, brand_id):
        """
        Returns warehouse keepers by a specific brand using the custom queryset.
        """
        return self.get_queryset().by_brand(brand_id)

    def active_products(self):
        """
        Returns warehouse keepers with active products using the custom queryset.
        """
        return self.get_queryset().active_products()

    def not_active_products(self):
        """
        Returns warehouse keepers with inactive products using the custom queryset.
        """
        return self.get_queryset().not_active_products()

    def delete_products(self):
        """
        Deletes warehouse keepers with zero quantity products using the custom queryset.
        """
        return self.get_queryset().delete_products()

    def total_quantity_lower_than(self, value):
        """
        Returns warehouse keepers with a total quantity lower than the specified value using the custom queryset.
        """
        return self.get_queryset().total_quantity_lower_than(value)
