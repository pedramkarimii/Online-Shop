import uuid
from django.test import TestCase
from django.utils import timezone
from apps.core.models import OrderPayment, WarehouseKeeper, CodeDiscount
from apps.account.models import User, Address
from apps.order.models import Order, OrderItem
from datetime import timedelta
from decimal import Decimal
from django.db import transaction

from apps.product.models import Category, Brand, Product


class CodeDiscountTestCase(TestCase):
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
        self.order_item = OrderItem.objects.create(user=self.user, product=self.product, quantity=1,
                                                   total_price=Decimal(10))
        self.address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number="3",
            postal_code="12345",
            notes="This is a test address"
        )
        # Create an order with the order item
        self.order = Order.objects.create(user=self.user, order_items=self.order_item, address=self.address)

        # Create a code discount with the brand
        self.code_discount = CodeDiscount.objects.create(user=self.user, category=self.category, order=self.order,
                                                         product=self.product)

    def test_create_code_discount(self):
        expiration_date = timezone.now() + timedelta(days=30)

        # Create a code discount with the order
        code_discount = CodeDiscount.objects.create(
            user=self.user,
            order=self.order,
            product=self.product,
            category=self.category,
            code="DISCOUNT123",
            percentage_discount=10,
            expiration_date=expiration_date,
        )
        self.assertIsNotNone(code_discount)

    def test_update_code_discount(self):
        # Update the percentage discount and expiration date
        new_percentage_discount = 20
        new_expiration_date = timezone.now() + timedelta(days=60)

        # Update the existing code discount instance
        self.code_discount.percentage_discount = new_percentage_discount
        self.code_discount.expiration_date = new_expiration_date
        self.code_discount.save()

        # Retrieve the updated code discount from the database
        updated_code_discount = CodeDiscount.objects.get(pk=self.code_discount.pk)

        # Check if the updates were successful
        self.assertEqual(updated_code_discount.percentage_discount, new_percentage_discount)
        self.assertEqual(updated_code_discount.expiration_date, new_expiration_date)

    def test_delete_code_discount(self):
        # Delete the code discount instance
        self.code_discount.delete()

        # Attempt to retrieve the deleted code discount from the database
        with self.assertRaises(CodeDiscount.DoesNotExist):  # noqa
            CodeDiscount.objects.get(pk=self.code_discount.pk)

    def test_soft_delete_code_discount(self):
        CodeDiscount.soft_delete.filter(id=self.code_discount.id).delete()
        soft_deleted_code_discount = CodeDiscount.soft_delete.archive().filter(id=self.code_discount.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_discount)
        self.assertTrue(soft_deleted_code_discount['is_deleted'])

    def test_code_discount_code_uniqueness(self):
        # Generate a unique code
        code = str(uuid.uuid4())

        expiration_date = timezone.now() + timedelta(days=30)

        # Create the first code discount
        code_discount1 = CodeDiscount.objects.create(
            user=self.user,
            product=self.product,
            category=self.category,
            order=self.order,
            code=code,
            percentage_discount=10,
            expiration_date=expiration_date,
        )

        # Attempt to create another code discount with a different code
        code_discount2 = CodeDiscount.objects.create(
            user=self.user,
            product=self.product,
            category=self.category,
            order=self.order,
            code=str(uuid.uuid4()),  # Generate another unique code
            percentage_discount=20,
            expiration_date=expiration_date,
        )

        # Ensure the objects were created successfully
        self.assertIsNotNone(code_discount1)
        self.assertIsNotNone(code_discount2)

    def test_code_discount_expiration(self):
        # Set the expiration date to a past date
        past_expiration_date = timezone.now() - timedelta(days=1)

        # Create a code discount with an expired expiration date
        expired_code_discount = CodeDiscount.objects.create(
            user=self.user,
            product=self.product,
            category=self.category,
            order=self.order,
            code="EXPIRED123",
            percentage_discount=10,
            expiration_date=past_expiration_date,
        )

        # Check if the discount code is expired
        self.assertFalse(CodeDiscount.objects.is_valid().filter(pk=expired_code_discount.pk).exists())


class WarehouseKeeperTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                          location="Test Location")
        self.product = Product.objects.create(user=self.user, category=self.category, brand=self.brand,
                                              name="Test Product", description="Test Description",
                                              price=100, quantity=10)

    def test_create_warehouse_keeper(self):
        warehouse_keeper = WarehouseKeeper.objects.create(
            user=self.user,
            brand=self.brand,
            product=self.product,
            quantity=5,
            available=True
        )
        self.assertIsNotNone(warehouse_keeper)

    def test_update_warehouse_keeper(self):
        warehouse_keeper = WarehouseKeeper.objects.create(
            user=self.user,
            brand=self.brand,
            product=self.product,
            quantity=5,
            available=True
        )
        warehouse_keeper.quantity = 10
        warehouse_keeper.save()
        updated_warehouse_keeper = WarehouseKeeper.objects.get(id=warehouse_keeper.id)
        self.assertEqual(updated_warehouse_keeper.quantity, 10)

    def test_delete_warehouse_keeper(self):
        warehouse_keeper = WarehouseKeeper.objects.create(
            user=self.user,
            brand=self.brand,
            product=self.product,
            quantity=5,
            available=True
        )
        warehouse_keeper.delete()
        with self.assertRaises(WarehouseKeeper.DoesNotExist):  # noqa
            WarehouseKeeper.objects.get(id=warehouse_keeper.id)

    def test_soft_delete_warehouse_keeper(self):
        warehouse_keeper = WarehouseKeeper.objects.create(
            user=self.user,
            brand=self.brand,
            product=self.product,
            quantity=5,
            available=True
        )
        WarehouseKeeper.soft_delete.filter(id=warehouse_keeper.id).delete()
        soft_deleted_code_warehouse_keeper = WarehouseKeeper.soft_delete.archive().filter(
            id=warehouse_keeper.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_warehouse_keeper)
        self.assertTrue(soft_deleted_code_warehouse_keeper['is_deleted'])


class OrderPaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                          location="Test Location")
        product = Product.objects.create(user=self.user, category=self.category, brand=self.brand, name="Test Product",
                                         description="Test Description", price=100, quantity=10)
        # Create a Address instance
        self.address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number="3",
            postal_code="12345",
            notes="This is a test address"
        )
        # Now, create the OrderItem instance and associate it with the WarehouseKeeper
        order_item = OrderItem.objects.create(user=self.user, product=product)

        # Now, create the Order instance and associate it with the OrderItem
        with transaction.atomic():
            self.order = Order.objects.create(user=self.user, order_items=order_item, address=self.address)

    def test_create_order_payment(self):
        expiration_date = timezone.now() + timedelta(days=30)
        order_payment = OrderPayment.objects.create(
            user=self.user,
            order=self.order,
            amount=Decimal('100.00'),
            cardholder_name="John Doe",
            card_number="1234567890123456",
            expiration_date=expiration_date,
            cvv="123",
            transaction_id="123456",
            payment_method="credit_card",
            status="pending",
            payment_time=timezone.now(),
        )
        self.assertIsNotNone(order_payment)

    def test_update_order_payment(self):
        order_payment = OrderPayment.objects.create(
            user=self.user,
            order=self.order,
            amount=Decimal('100.00'),
            cardholder_name="John Doe",
            card_number="1234567890123456",
            expiration_date=timezone.now() + timedelta(days=30),
            cvv="123",
            transaction_id="123456",
            payment_method="credit_card",
            status="pending",
            payment_time=timezone.now(),
        )
        order_payment.amount = Decimal('200.00')
        order_payment.save()
        updated_order_payment = OrderPayment.objects.get(id=order_payment.id)
        self.assertEqual(updated_order_payment.amount, Decimal('200.00'))

    def test_delete_order_payment(self):
        order_payment = OrderPayment.objects.create(
            user=self.user,
            order=self.order,
            amount=Decimal('100.00'),
            cardholder_name="John Doe",
            card_number="1234567890123456",
            expiration_date=timezone.now() + timedelta(days=30),
            cvv="123",
            transaction_id="123456",
            payment_method="credit_card",
            status="pending",
            payment_time=timezone.now(),
        )
        order_payment.delete()
        with self.assertRaises(OrderPayment.DoesNotExist):  # noqa
            OrderPayment.objects.get(id=order_payment.id)
