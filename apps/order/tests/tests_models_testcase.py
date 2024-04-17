from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.core.models import WarehouseKeeper, CodeDiscount
from apps.order.models import StatusOrder, Order, OrderItem
from apps.account.models import User
from apps.product.models import Category, Brand, Product


class OrderItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand")

        # Create a product
        self.product = Product.objects.create(user=self.user, category=self.category, brand=self.brand,
                                              name="Test Product")

        # Create a warehouse keeper with the product
        self.warehouse_keeper = WarehouseKeeper.objects.create(user=self.user, brand=self.brand, product=self.product)

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            warehouse_keeper=self.warehouse_keeper,
            total_price=Decimal(10),
            quantity=1
        )
        self.assertIsNotNone(order_item)

    def test_update_order_item(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            warehouse_keeper=self.warehouse_keeper,
            total_price=Decimal(10),
            quantity=1
        )
        # Update fields and save
        order_item.quantity = 2
        order_item.save()
        # Retrieve the updated instance and verify the changes
        updated_order_item = OrderItem.objects.get(id=order_item.id)
        self.assertEqual(updated_order_item.quantity, 2)

    def test_delete_order_item(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            warehouse_keeper=self.warehouse_keeper,
            total_price=Decimal(10),
            quantity=1
        )
        order_item.delete()
        # Try to retrieve the deleted instance, it should raise a DoesNotExist exception
        with self.assertRaises(OrderItem.DoesNotExist):  # noqa
            OrderItem.objects.get(id=order_item.id)


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand")
        self.product = Product.objects.create(user=self.user, category=self.category, brand=self.brand,
                                              name="Test Product")
        self.warehouse_keeper = WarehouseKeeper.objects.create(user=self.user, brand=self.brand, product=self.product)

    def test_create_order(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            warehouse_keeper=self.warehouse_keeper,
            total_price=Decimal(10),
            quantity=1
        )
        order = Order.objects.create(
            user=self.user,
            order_items=order_item,
            status='new'
        )
        self.assertIsNotNone(order)

    def test_update_order(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            warehouse_keeper=self.warehouse_keeper,
            total_price=Decimal(10),
            quantity=1
        )
        order = Order.objects.create(
            user=self.user,
            order_items=order_item,
            status='new'
        )
        # Update fields and save
        order.status = 'paid'
        order.save()
        # Retrieve the updated instance and verify the changes
        updated_order = Order.objects.get(id=order.id)
        self.assertEqual(updated_order.status, 'paid')

    def test_delete_order(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            warehouse_keeper=self.warehouse_keeper,
            total_price=Decimal(10),
            quantity=1
        )
        order = Order.objects.create(
            user=self.user,
            order_items=order_item,
            status='new'
        )
        order.delete()
        # Try to retrieve the deleted instance, it should raise a DoesNotExist exception
        with self.assertRaises(Order.DoesNotExist):  # noqa
            Order.objects.get(id=order.id)


class StatusOrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand")

        # Create a product
        self.product = Product.objects.create(user=self.user, category=self.category, brand=self.brand,
                                              name="Test Product")

        # Create a warehouse keeper with the product
        self.warehouse_keeper = WarehouseKeeper.objects.create(user=self.user, brand=self.brand, product=self.product)

        # Assuming you have a valid OrderItem instance named 'order_item'
        self.order_item = OrderItem.objects.create(user=self.user, product=self.product,
                                                   warehouse_keeper=self.warehouse_keeper, quantity=1,
                                                   total_price=Decimal(10))

        # Create an order with the order item
        self.order = Order.objects.create(user=self.user, order_items=self.order_item)

        # Create a code discount with the brand
        self.code_discount = CodeDiscount.objects.create(user=self.user, category=self.category, order=self.order,
                                                         product=self.product)

    def test_create_status_order(self):
        status_order = StatusOrder.objects.create(
            user=self.user,
            order=self.order,
            time_accepted_order=timezone.now(),
            accepted_order=True,
            time_shipped_order=timezone.now(),
            shipped_order=True,
            time_deliver_order=timezone.now(),
            deliver_order=True,
            time_rejected_order=timezone.now(),
            rejected_order=True,
            time_cancelled_order=timezone.now(),
            cancelled_order=True,
            deliver=True
        )
        self.assertIsNotNone(status_order)

    def test_update_status_order(self):
        status_order = StatusOrder.objects.create(
            user=self.user,
            order=self.order,
            time_accepted_order=timezone.now(),
            accepted_order=True
        )
        # Update fields and save
        status_order.accepted_order = False
        status_order.save()
        # Retrieve the updated instance and verify the changes
        updated_status_order = StatusOrder.objects.get(id=status_order.id)
        self.assertFalse(updated_status_order.accepted_order)

    def test_delete_status_order(self):
        status_order = StatusOrder.objects.create(
            user=self.user,
            order=self.order,
            time_accepted_order=timezone.now(),
            accepted_order=True
        )
        status_order.delete()
        # Try to retrieve the deleted instance, it should raise a DoesNotExist exception
        with self.assertRaises(StatusOrder.DoesNotExist):  # noqa
            StatusOrder.objects.get(id=status_order.id)
