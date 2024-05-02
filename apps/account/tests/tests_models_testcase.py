from django.test import TestCase
from apps.account.models import Address, CodeDiscount, UserAuth
from django.contrib.auth import get_user_model
from datetime import date
from datetime import datetime, timedelta
import uuid

User = get_user_model()


class TestUserAuthModel(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "pedramkarimi",
            "email": "pedram.9060@example.com",
            "phone_number": "09128355747",
            "name": "pedram",
            "last_name": "karimi",
            "gender": "Male",
            "age": 30,
            "profile_picture": None,
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_auth_create(self):
        UserAuth.objects.create(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())
        self.assertEqual(UserAuth.objects.count(), 1)

    def test_ordering_user_auth(self):
        for i in range(10):
            UserAuth.objects.create(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())

        self.assertEqual(UserAuth.objects.first().id, 10)


class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone_number": "09123456789",
            "name": "Test",
            "last_name": "User",
            "gender": "Male",
            "age": 30,
            "profile_picture": None,
            "is_deleted": False,
            "is_admin": False,
            "is_staff": False,
            "is_superuser": False,
        }
        self.user = User.objects.create(**self.user_data)

    def test_unique_fields(self):
        # Attempt to create a user with the same username, email, and phone number
        duplicate_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone_number": "09123456789",
            "name": "Test",
            "last_name": "User",
            "gender": "Male",
            "age": 30,
            "profile_picture": None,
            "is_deleted": False,
            "is_admin": False,
            "is_staff": False,
            "is_superuser": False,
        }
        with self.assertRaises(Exception):
            User.objects.create(**duplicate_user_data)

    def test_create_user(self):
        # Check if the user is created successfully
        created_user = User.objects.get(username="testuser")
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, self.user_data["username"])
        self.assertEqual(created_user.email, self.user_data["email"])
        self.assertEqual(created_user.phone_number, self.user_data["phone_number"])

    def test_update_user(self):
        # Update user's information
        updated_data = {
            "name": "Updated",
            "last_name": "User",
            "age": 35,
        }
        self.user.name = updated_data["name"]
        self.user.last_name = updated_data["last_name"]
        self.user.age = updated_data["age"]
        self.user.save()

        # Retrieve the updated user from the database
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.name, updated_data["name"])
        self.assertEqual(updated_user.last_name, updated_data["last_name"])
        self.assertEqual(updated_user.age, updated_data["age"])

    def test_delete_user(self):
        # Delete the user
        self.user.delete()

        # Check if the user is deleted successfully
        with self.assertRaises(User.DoesNotExist):  # noqa
            User.objects.get(username="testuser")

    def test_soft_delete_user(self):
        # Print initial state (optional)
        print('Initial is_deleted:', self.user.is_deleted)

        # Soft delete the user
        User.soft_delete.filter(id=self.user.id).delete()

        # Check if the user is soft deleted
        soft_deleted_user = User.soft_delete.archive().filter(id=self.user.id).values('is_deleted').first()

        # Assert the soft deleted user is not None
        self.assertIsNotNone(soft_deleted_user)

        # Assert that is_deleted field is True
        self.assertTrue(soft_deleted_user['is_deleted'])


class AddressModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            phone_number="09123456789",
            name="John",
            last_name="Doe",
            gender="Male",
            age=30
        )

    def test_address_uniqueness(self):
        # Create an address
        Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )

        # Attempt to create another address with the same user and address name
        with self.assertRaises(Exception):
            Address.objects.create(
                user=self.user,
                address_name="Home",
                country="Iran",
                city="Tehran",
                street="456 Elm St",
                building_number="5B",
                floor_number=4,
                postal_code=54321,
                notes="Another test address"
            )

    def test_address_creation(self):
        # Create an address
        address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )

        # Check if address was created successfully
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.address_name, "Home")
        self.assertEqual(address.country, "Iran")
        self.assertEqual(address.city, "Tehran")
        self.assertEqual(address.street, "123 Main St")
        self.assertEqual(address.building_number, "5A")
        self.assertEqual(address.floor_number, 3)
        self.assertEqual(address.postal_code, 12345)
        self.assertEqual(address.notes, "This is a test address")

    def test_address_update(self):
        # Create an address
        address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )

        # Update the address
        address.street = "456 Elm St"
        address.save()

        # Retrieve the updated address from the database
        updated_address = Address.objects.get(id=address.id)

        # Check if the address was updated successfully
        self.assertEqual(updated_address.street, "456 Elm St")

    def test_address_deletion(self):
        # Create an address
        address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )

        # Delete the address
        address.delete()

        # Check if the address was deleted successfully
        with self.assertRaises(Address.DoesNotExist):  # noqa
            Address.objects.get(id=address.id)

    def test_soft_delete(self):
        # Create an address
        address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )

        # Soft delete the address
        Address.soft_delete.filter(id=address.id).delete()

        # Retrieve the soft deleted address
        soft_deleted_address = Address.soft_delete.archive().filter(id=address.id).first()

        # Assert that the soft deleted address is retrieved
        self.assertIsNotNone(soft_deleted_address)
        self.assertTrue(soft_deleted_address.is_deleted)

    def test_address_str_representation(self):
        # Create an address
        address = Address.objects.create(
            user=self.user,
            address_name="Home",
            country="Iran",
            city="Tehran",
            street="123 Main St",
            building_number="5A",
            floor_number=3,
            postal_code=12345,
            notes="This is a test address"
        )

        # Check the string representation of the address
        self.assertEqual(str(address), f'{address.user} - {address.address_name}')


class CodeDiscountModelTestCase(TestCase):

    def setUp(self):
        # Create a sample user for testing
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            phone_number="09123456789",
            name="John",
            last_name="Doe",
            gender="Male",
            age=30
        )

    def test_create_discount_code(self):
        # Create a discount code
        discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="TESTCODE",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today()
        )
        # Assert that the discount code is created successfully
        self.assertEqual(discount_code.code, "TESTCODE")

    def test_update_discount_code(self):
        # Create a discount code
        discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="TESTCODE",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today()
        )
        # Update the discount code
        discount_code.code = "UPDATEDCODE"
        discount_code.save()
        # Retrieve the updated discount code from the database
        updated_discount_code = CodeDiscount.objects.get(id=discount_code.id)
        # Assert that the code is updated successfully
        self.assertEqual(updated_discount_code.code, "UPDATEDCODE")

    def test_delete_discount_code(self):
        # Create a discount code
        discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="TESTCODE",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today()
        )
        # Delete the discount code
        discount_code.delete()
        # Assert that the discount code is deleted successfully
        with self.assertRaises(CodeDiscount.DoesNotExist):  # noqa
            CodeDiscount.objects.get(id=discount_code.id)

    def test_is_expired(self):
        # Create a discount code that has expired
        expired_date = datetime.now().date() - timedelta(days=1)
        expired_code = CodeDiscount.objects.create(
            user=self.user,
            code="EXPIRED",
            percentage_discount=10,
            expiration_date=expired_date,
            is_expired=False  # This should be False initially
        )

        if expired_code.expiration_date < datetime.now().date():
            expired_code.is_expired = True

        # Check if the code is marked as expired
        self.assertTrue(expired_code.is_expired)

        # Create a discount code that has not expired
        valid_code = CodeDiscount.objects.create(
            user=self.user,
            code="VALID",
            percentage_discount=20,
            expiration_date=datetime.now() + timedelta(days=1),
            is_expired=False  # This should be False initially
        )

        # Check if the code is not marked as expired
        self.assertFalse(valid_code.is_expired)

    def test_is_not_expired(self):
        # Create a discount code with an expiration date in the future
        active_discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="ACTIVECODE",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today()  # Set expiration date in the future
        )
        # Assert that the discount code is not expired
        self.assertFalse(active_discount_code.is_expired)

    def test_is_used(self):
        # Create a discount code that has been used
        used_discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="USEDCODE",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today(),
            is_use=1  # Set is_use to 1 indicating it has been used
        )
        # Assert that the discount code has been used
        self.assertTrue(used_discount_code.is_use)

    def test_is_not_used(self):
        # Create a discount code that has not been used
        unused_discount_code = CodeDiscount.objects.create(
            user=self.user,
            code="UNUSED",
            percentage_discount=10,
            numerical_discount=50,
            expiration_date=date.today(),
            is_use=0  # Set is_use to 0 indicating it has not been used
        )
        # Assert that the discount code has not been used
        self.assertFalse(unused_discount_code.is_use)
