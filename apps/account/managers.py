from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.postgres.search import TrigramSimilarity
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, username, password):
        """
        Creates and saves a regular user with the given phone number, email, username, and password.
        """
        if not phone_number:
            raise ValueError('The phone number must be set')
        elif not email:
            raise ValueError('The Email must be set')
        elif not username:
            raise ValueError('The username must be set')
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), username=username)
        user.is_admin = False
        user.is_superuser = False
        user.is_superuser = False
        user.set_password(password)
        user.save()
        return user

    def create_admin(self, phone_number, email, username, password):
        """
        Creates and saves an admin user with the given phone number, email, username, and password.
        """
        user = self.create_user(phone_number, email, username, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = False
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, email, username, password):
        """
        Creates and saves a superuser with the given phone number, email, username, and password.
        """
        user = self.create_user(phone_number, email, username, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class UserAuthQuerySet(models.QuerySet):
    pass


class UserAuthManager(models.Manager):
    """Manager for handling address operations."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = UserAuthQuerySet(self.model)
        return self.__queryset


class ProfileQuerySet(models.QuerySet):
    pass


class ProfileManager(models.Manager):
    """Manager for handling address operations."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = UserAuthQuerySet(self.model)
        return self.__queryset


class AddressQuerySet(models.QuerySet):
    """QuerySet for handling address operations."""

    def active_addresses(self):
        """Retrieve active addresses."""
        return self.filter(active=True)

    def inactive_addresses(self):
        """Retrieve inactive addresses."""
        return self.filter(active=False)

    def search_address(self, keyword):
        """Search for addresses based on a keyword."""
        return self.annotate(similarity=TrigramSimilarity('address_name', keyword)).filter(similarity__gt=0.3).order_by(
            '-similarity')

    def user_addresses(self, user):
        """Retrieve addresses associated with a specific user."""
        return self.filter(user=user)

    def address_summary(self):
        """Generate a summary of addresses."""
        return self.annotate(total=models.Count('id')).order_by('-total')

    def update_address(self, address_id, **kwargs):
        """Update an existing address."""
        return self.filter(pk=address_id).update(**kwargs)

    def create_address(self, user, **kwargs):
        """Create a new address."""
        return self.create(user=user, **kwargs)


class AddressManager(models.Manager):
    """Manager for handling address operations."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = AddressQuerySet(self.model)
        return self.__queryset

    def active_addresses(self):
        """Retrieve active addresses."""
        return self.get_queryset().active_addresses()

    def inactive_addresses(self):
        """Retrieve inactive addresses."""
        return self.get_queryset().inactive_addresses()

    def search_address(self, keyword):
        """Search for addresses based on a keyword."""
        return self.get_queryset().search_address(keyword)

    def create_address(self, user, **kwargs):
        """Create a new address."""
        return self.get_queryset().create_address(user, **kwargs)

    def update_address(self, address_id, **kwargs):
        """Update an existing address."""
        return self.get_queryset().update_address(address_id, **kwargs)

    def address_summary(self):
        """Generate a summary of addresses."""
        return self.get_queryset().address_summary()


class RoleQuerySet(models.QuerySet):
    pass


class RoleManager(models.Manager):
    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = RoleQuerySet(self.model)
        return self.__queryset


class CodeDiscountQuerySet(models.QuerySet):
    def active_discounts(self):
        """
        Filters queryset to retrieve only active discount codes.
        """
        return self.filter(
            expiration_date__gt=models.DateField(auto_now_add=True),
            is_use=0,
            is_expired=False
        )

    def create_discount_code(self, user, code, percentage_discount=None, numerical_discount=None, expiration_date=None):
        """
        Creates a new discount code.
        """
        return self.create(
            user=user,
            code=code,
            percentage_discount=percentage_discount,
            numerical_discount=numerical_discount,
            expiration_date=expiration_date
        )

    def update_discount_code(self, code, **kwargs):
        """
        Updates a discount code.
        """
        return self.filter(code=code).update(**kwargs)

    def used_discounts_search(self, keyword):
        """
        Searches for used discount codes.
        """
        return self.filter(
            user__username__icontains=keyword,
            is_use=1,
            is_expired=False
        )

    def expired_discounts(self):
        """
        Filters queryset to retrieve expired discount codes.
        """
        return self.filter(
            expiration_date__lte=models.DateField(auto_now_add=True),
            is_use=0,
            is_expired=False
        )

    def search_by_code(self, code):
        """
        Filters queryset to retrieve discount codes by code.
        """
        return self.filter(code__icontains=code)

    def numerical_discount_gt(self, value):
        """
        Filters queryset to retrieve discount codes with numerical discount greater than the specified value.
        """
        return self.filter(numerical_discount__gt=value)

    def numerical_discount_lt(self, value):
        """
        Filters queryset to retrieve discount codes with numerical discount less than the specified value.
        """
        return self.filter(numerical_discount__lt=value)

    def percentage_discount_gt(self, value):
        """
        Filters queryset to retrieve discount codes with percentage discount greater than the specified value.
        """
        return self.filter(percentage_discount__gt=value)


class CodeDiscountManager(models.Manager):
    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = CodeDiscountQuerySet(self.model)
        return self.__queryset

    @property
    def is_expired(self):
        """
        Property to check if the discount code is expired.
        """
        # Check if expiration_date is set
        if self.expiration_date:
            print('A' * 300, "Expiration Date:", self.expiration_date)
            # Check if expiration_date is in the past
            if self.expiration_date < timezone.now().date():
                return True
        return False

    def create_discount_code(self, user, code, percentage_discount=None, numerical_discount=None, expiration_date=None):
        """
        Creates a new discount code.
        """
        return self.get_queryset().create_discount_code(user, code, percentage_discount, numerical_discount,
                                                        expiration_date)

    def update_discount_code(self, code, **kwargs):
        """
        Updates a discount code.
        """
        return self.get_queryset().update_discount_code(code, **kwargs)

    def get_active_discounts(self):
        """
        Retrieves all active discount codes.
        """
        return self.get_queryset().active_discounts()

    def get_used_discounts(self):
        """
        Retrieves all used discount codes.
        """
        return self.get_queryset().used_discounts_search()

    def get_expired_discounts(self):
        """
        Retrieves all expired discount codes.
        """
        return self.get_queryset().expired_discounts()

    def search_discounts_by_code(self, code):
        """
        Searches discount codes by code.
        """
        return self.get_queryset().search_by_code(code)

    def get_discounts_with_numerical_discount_gt(self, value):
        """
        Retrieves discount codes with numerical discount greater than the specified value.
        """
        return self.get_queryset().numerical_discount_gt(value)

    def get_discounts_with_percentage_discount_gt(self, value):
        """
        Retrieves discount codes with percentage discount greater than the specified value.
        """
        return self.get_queryset().percentage_discount_gt(value)
