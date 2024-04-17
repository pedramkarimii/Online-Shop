from django.db import models
from django.db.models import Case, When, Value, BooleanField, IntegerField, ExpressionWrapper, DecimalField, Sum
from django.db.models import F
from django.db.models.functions import Coalesce
from django.utils import timezone


class OrderItemQuerySet(models.QuerySet):
    def with_discount(self):
        """
        Annotate the queryset with a boolean indicating whether each order item has a discount applied.
        """
        return self.annotate(
            has_discount=Case(
                When(product__code_discount__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def total_price_each_product_with_discount(self):
        """
        Annotate the queryset with the total price for each product considering any code discounts.
        """
        return self.annotate(
            total_price_each_product_with_discount=ExpressionWrapper(
                F('price') - Coalesce(
                    F('price') * F('product__code_discount__percentage_discount') / 100,
                    F('product__code_discount__numerical_discount'),
                    F('price')
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

    def total_price_without_discount(self):
        """
        Annotate the queryset with the total price for each product without considering any code discounts.
        """
        return self.annotate(
            total_price_without_discount=F('price') * F('quantity')
        )

    def total_price_each_product(self):
        """
        Annotate the queryset with the total price for each product, considering whether a discount is applied.
        """
        return self.with_discount().annotate(
            total_price_each_product=Case(
                When(has_discount=True, then=F('total_price_each_product_with_discount')),
                default=F('total_price_without_discount'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

    def total_price_ordered(self):
        """
        Calculate the total price of all order items, considering any code discounts.
        """
        return self.aggregate(
            total_price_ordered=Coalesce(Sum(F('total_price_each_product')), Value(0))
        )['total_price_ordered']


class OrderItemManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = OrderItemQuerySet(self.model)
        return self.__queryset

    def total_price_each_product(self):
        """
        Calculate the total price for each product, considering any code discounts.
        """
        return self.get_queryset().total_price_each_product()

    def total_price_ordered(self):
        """
        Calculate the total price of all order items, considering any code discounts.
        """
        return self.get_queryset().total_price_ordered()


class OrderQuerySet(models.QuerySet):
    def with_total_quantity_ordered(self):
        """
        Annotate the queryset with the total quantity of all order items in each order.
        """
        return self.annotate(
            total_quantity_ordered=Sum('order_items__quantity')
        )

    def with_total_price(self):
        """
        Annotate the queryset with the total price of each order.
        """
        return self.annotate(
            total_price=Sum('order_items__total_price_each_product')
        )

    def with_total_discount(self):
        """
        Annotate the queryset with the total discount applied to each order.
        """
        return self.annotate(
            total_discount=Sum(
                Case(
                    When(order_items__product__code_discount__percentage_discount__isnull=False,
                         then=(F('order_items__price') * F('order_items__quantity') *
                               F('order_items__product__code_discount__percentage_discount') / 100)),
                    When(order_items__product__code_discount__numerical_discount__isnull=False,
                         then=F('order_items__product__code_discount__numerical_discount')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            )
        )

    def with_is_discounted(self):
        """
        Annotate the queryset with a boolean indicating whether each order has a discount applied.
        """
        return self.annotate(
            is_discounted=Case(
                When(total_discount__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def orders_within_last_30_days(self):
        """
        Return orders placed within the last 30 days.
        """
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        return self.filter(created_at__gte=thirty_days_ago)


class OrderManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = OrderQuerySet(self.model)
        return self.__queryset

    def with_total_quantity_ordered(self):
        """
        Annotate the queryset with the total quantity of all order items in each order.
        """
        return self.get_queryset().with_total_quantity_ordered()

    def with_total_price(self):
        """
        Annotate the queryset with the total price of each order.
        """
        return self.get_queryset().with_total_price()

    def with_total_discount(self):
        """
        Annotate the queryset with the total discount applied to each order.
        """
        return self.get_queryset().with_total_discount()

    def with_is_discounted(self):
        """
        Annotate the queryset with a boolean indicating whether each order has a discount applied.
        """
        return self.get_queryset().with_is_discounted()

    def orders_within_last_30_days(self):
        """
        Return orders placed within the last 30 days.
        """
        return self.get_queryset().orders_within_last_30_days()


class StatusOrderQuerySet(models.QuerySet):
    def accepted_orders(self):
        """
        Filter queryset to retrieve accepted orders.
        """
        return self.filter(accepted_order=True)

    def shipped_orders(self):
        """
        Filter queryset to retrieve shipped orders.
        """
        return self.filter(shipped_order=True)

    def delivered_orders(self):
        """
        Filter queryset to retrieve delivered orders.
        """
        return self.filter(deliver_order=True)

    def rejected_orders(self):
        """
        Filter queryset to retrieve rejected orders.
        """
        return self.filter(rejected_order=True)

    def cancelled_orders(self):
        """
        Filter queryset to retrieve cancelled orders.
        """
        return self.filter(cancelled_order=True)

    def completed_orders(self):
        """
        Filter queryset to retrieve completed orders.
        """
        return self.filter(deliver=True)


class StatusOrderManager(models.Manager):
    def get_queryset(self):
        """
        Get the queryset object associated with this manager.
        """
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = StatusOrderQuerySet(self.model)
        return self.__queryset

    def accepted_orders(self):
        """
        Retrieve queryset of accepted orders.
        """
        return self.get_queryset().accepted_orders()

    def shipped_orders(self):
        """
        Retrieve queryset of shipped orders.
        """
        return self.get_queryset().shipped_orders()

    def delivered_orders(self):
        """
        Retrieve queryset of delivered orders.
        """
        return self.get_queryset().delivered_orders()

    def rejected_orders(self):
        """
        Retrieve queryset of rejected orders.
        """
        return self.get_queryset().rejected_orders()

    def cancelled_orders(self):
        """
        Retrieve queryset of cancelled orders.
        """
        return self.get_queryset().cancelled_orders()

    def completed_orders(self):
        """
        Retrieve queryset of completed orders.
        """
        return self.get_queryset().completed_orders()
