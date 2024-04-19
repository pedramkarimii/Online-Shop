from django.test import TestCase
from apps.account.models import User
from apps.product.models import Brand, Media, Category, Product, Comment


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
