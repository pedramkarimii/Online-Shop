from datetime import timedelta, date
from decimal import Decimal
from django.db import transaction
from django.test import TestCase
from django.utils import timezone
from apps.order.models import Order, OrderItem, OrderPayment
from apps.account.models import User, Address, CodeDiscount
from apps.product.models import Category, Brand, Product, WarehouseKeeper


class OrderItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand")

        # Create a product
        self.product = Product.objects.create(category=self.category, brand=self.brand,
                                              name="Test Product")
        self.address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number=5,
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )
        self.order = Order.objects.create(
            address=self.address,
            status='Paid'
        )

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            product=self.product,
            order=self.order,
            total_price=Decimal(10),
            quantity=1
        )
        self.assertIsNotNone(order_item)

    def test_update_order_item(self):
        order_item = OrderItem.objects.create(
            user=self.user,
            order=self.order,
            product=self.product,
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
            order=self.order,
            product=self.product,
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
        self.product = Product.objects.create(category=self.category, brand=self.brand,
                                              name="Test Product")
        self.discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="TESTCODE",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today()
        )
        self.address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number=5,
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )
        self.warehouse_keeper = WarehouseKeeper.objects.create(user=self.user, brand=self.brand, product=self.product)

    def test_create_order(self):
        order = Order.objects.create(
            address=self.address,
            status='new'
        )
        self.assertIsNotNone(order)

    def test_update_order(self):
        order = Order.objects.create(
            address=self.address,
            status='paid',
        )

        # Update fields and save
        order.status = 'Cancelled'
        order.save()

        # Retrieve the updated instance and verify the changes
        updated_order = Order.objects.get(id=order.id)
        self.assertEqual(updated_order.status, 'Cancelled')

    def test_delete_order(self):
        order = Order.objects.create(
            address=self.address,
            status='new'
        )
        order.delete()
        # Try to retrieve the deleted instance, it should raise a DoesNotExist exception
        with self.assertRaises(Order.DoesNotExist):  # noqa
            Order.objects.get(id=order.id)


class OrderPaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                          location="Test Location")

        self.address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number=5,
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )
        self.order = Order.objects.create(
            address=self.address,
            status='Paid'
        )

        # Now, create the Order instance and associate it with the OrderItem
        with transaction.atomic():
            self.order = Order.objects.create(
                address=self.address,
                status='Paid'
            )

    def test_create_order_payment(self):
        expiration_date = timezone.now() + timedelta(days=30)
        order_payment = OrderPayment.objects.create(
            order=self.order,
            amount=Decimal('100.00'),
            cardholder_name="John Doe",
            card_number="1234567890123456",
            expiration_date=expiration_date,
            cvv="123",
            status="pending",
            payment_time=timezone.now(),
        )
        self.assertIsNotNone(order_payment)

    def test_update_order_payment(self):
        order_payment = OrderPayment.objects.create(
            order=self.order,
            amount=Decimal('100.00'),
            cardholder_name="John Doe",
            card_number="1234567890123456",
            expiration_date=timezone.now() + timedelta(days=30),
            cvv="123",
            status="pending",
            payment_time=timezone.now(),
        )
        order_payment.amount = Decimal('200.00')
        order_payment.save()
        updated_order_payment = OrderPayment.objects.get(id=order_payment.id)
        self.assertEqual(updated_order_payment.amount, Decimal('200.00'))

    def test_delete_order_payment(self):
        order_payment = OrderPayment.objects.create(
            order=self.order,
            amount=Decimal('100.00'),
            cardholder_name="John Doe",
            card_number="1234567890123456",
            expiration_date=timezone.now() + timedelta(days=30),
            cvv="123",
            status="pending",
            payment_time=timezone.now(),
        )
        order_payment.delete()
        with self.assertRaises(OrderPayment.DoesNotExist):  # noqa
            OrderPayment.objects.get(id=order_payment.id)
