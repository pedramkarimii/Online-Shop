from django.test import TestCase
from apps.account.models import User, Address
from apps.order.models import OrderItem, Order
from apps.product.models import Brand, Media, Category, Product, Comment, WarehouseKeeper, CodeDiscount
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
import uuid


class BrandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")

    def test_create_brand(self):
        brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                     location="Test Location")
        self.assertIsNotNone(brand)

    def test_update_brand(self):
        brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                     location="Test Location")
        brand.name = "Updated Brand Name"
        brand.save()
        updated_brand = Brand.objects.get(id=brand.id)
        self.assertEqual(updated_brand.name, "Updated Brand Name")

    def test_delete_brand(self):
        brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                     location="Test Location")
        brand.delete()
        with self.assertRaises(Brand.DoesNotExist):  # noqa
            Brand.objects.get(id=brand.id)

    def test_delete_brand_cascade(self):
        brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                     location="Test Location")
        product = Product.objects.create(user=self.user, category=Category.objects.create(name="Test Category"),
                                         brand=brand, name="Test Product", description="Test Description",
                                         price=100, quantity=10)
        Brand.soft_delete.filter(id=brand.id).delete()  # Accessing soft_delete manager via model class

        self.assertIsNotNone(brand)
        self.assertIsNotNone(product)

    def test_soft_delete_brand(self):
        brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                     location="Test Location")
        Brand.soft_delete.filter(id=brand.id).delete()
        soft_deleted_code_brand = Brand.soft_delete.archive().filter(id=brand.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_brand)
        self.assertTrue(soft_deleted_code_brand['is_deleted'])


class MediaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                          location="Test Location")
        self.product = Product.objects.create(user=self.user, category=self.category, brand=self.brand,
                                              name="Test Product", description="Test Description", price=100,
                                              quantity=10)

    def test_create_media(self):
        media = Media.objects.create(product=self.product, product_picture="test.jpg")
        self.assertIsNotNone(media)

    def test_update_media(self):
        media = Media.objects.create(product=self.product, product_picture="test.jpg")
        media.product_picture = "updated_test.jpg"
        media.save()
        updated_media = Media.objects.get(id=media.id)
        self.assertEqual(updated_media.product_picture, "updated_test.jpg")

    def test_delete_media(self):
        media = Media.objects.create(product=self.product, product_picture="test.jpg")
        media.delete()
        with self.assertRaises(Media.DoesNotExist):  # noqa
            Media.objects.get(id=media.id)

    def test_soft_delete_media(self):
        media = Media.objects.create(product=self.product, product_picture="tests.jpg")

        Media.soft_delete.filter(id=media.id).delete()
        soft_deleted_code_media = Media.soft_delete.archive().filter(id=media.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_media)
        self.assertTrue(soft_deleted_code_media['is_deleted'])


class CategoryTestCase(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Test Category")
        self.assertIsNotNone(category)

    def test_update_category(self):
        category = Category.objects.create(name="Test Category")
        category.name = "Updated Category"
        category.save()
        updated_category = Category.objects.get(id=category.id)
        self.assertEqual(updated_category.name, "Updated Category")

    def test_delete_category(self):
        category = Category.objects.create(name="Test Category")
        category.delete()
        with self.assertRaises(Category.DoesNotExist):  # noqa
            Category.objects.get(id=category.id)

    def test_delete_category_cascade(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        category = Category.objects.create(name="Test Category")
        brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                     location="Test Location")
        Product.objects.create(user=self.user, category=category, brand=brand, name="Test Product",
                               description="Test Description", price=100, quantity=10)
        Category.soft_delete.filter(id=category.id).delete()  # Accessing soft_delete manager via model class

        self.assertIsNotNone(category)
        self.assertIsNotNone(brand)
        self.assertIsNotNone(Product.objects.get(id=brand.id))

    def test_soft_delete_category(self):
        category = Category.objects.create(name="Test Category")
        Category.soft_delete.filter(id=category.id).delete()
        soft_deleted_code_category = Category.soft_delete.archive().filter(id=category.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_category)
        self.assertTrue(soft_deleted_code_category['is_deleted'])


class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                          location="Test Location")

    def test_create_product(self):
        product = Product.objects.create(user=self.user, category=self.category, brand=self.brand, name="Test Product",
                                         description="Test Description", price=100, quantity=10)
        self.assertIsNotNone(product)

    def test_update_product(self):
        product = Product.objects.create(user=self.user, category=self.category, brand=self.brand, name="Test Product",
                                         description="Test Description", price=100, quantity=10)
        product.name = "Updated Product"
        product.save()
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.name, "Updated Product")

    def test_delete_product(self):
        product = Product.objects.create(user=self.user, category=self.category, brand=self.brand, name="Test Product",
                                         description="Test Description", price=100, quantity=10)
        product.delete()
        with self.assertRaises(Product.DoesNotExist):  # noqa
            Product.objects.get(id=product.id)

    def test_soft_delete_product(self):
        product = Product.objects.create(user=self.user, category=self.category, brand=self.brand, name="Test Product",
                                         description="Test Description", price=100, quantity=10)

        Product.soft_delete.filter(id=product.id).delete()
        soft_deleted_code_product = Product.soft_delete.archive().filter(id=product.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_product)
        self.assertTrue(soft_deleted_code_product['is_deleted'])


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com")  # noqa
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(user=self.user, name="Test Brand", description="Test Description",
                                          location="Test Location")
        self.product = Product.objects.create(user=self.user, category=self.category, brand=self.brand,
                                              name="Test Product", description="Test Description", price=100,
                                              quantity=10)

    def test_create_comment(self):
        comment = Comment.objects.create(user=self.user, product=self.product, comment="Test Comment")
        self.assertIsNotNone(comment)

    def test_update_comment(self):
        comment = Comment.objects.create(user=self.user, product=self.product, comment="Test Comment")
        comment.comment = "Updated Comment"
        comment.save()
        updated_comment = Comment.objects.get(id=comment.id)
        self.assertEqual(updated_comment.comment, "Updated Comment")

    def test_delete_comment(self):
        comment = Comment.objects.create(user=self.user, product=self.product, comment="Test Comment")
        comment.delete()
        with self.assertRaises(Comment.DoesNotExist):  # noqa
            Comment.objects.get(id=comment.id)

    def test_soft_delete_comment(self):
        comment = Comment.objects.create(user=self.user, product=self.product, comment="Test Comment")

        Comment.soft_delete.filter(id=comment.id).delete()
        soft_deleted_code_comment = Comment.soft_delete.archive().filter(id=comment.id).values(
            'is_deleted').first()
        self.assertIsNotNone(soft_deleted_code_comment)
        self.assertTrue(soft_deleted_code_comment['is_deleted'])


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
