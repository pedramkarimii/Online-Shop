from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import F
from django.contrib.postgres.search import TrigramSimilarity


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

    def increment_floor_numbers(self):
        """Increment floor numbers for addresses."""
        return self.update(floor_number=F('floor_number') + 1)


class AddressManager(models.Manager):
    """Manager for handling address operations."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = AddressQuerySet(self.model)
        return self.__queryset

    def create_address(self, user, **kwargs):
        """Create a new address."""
        return self.create(user=user, **kwargs)

    def toggle_active(self, address_id, active=True):
        """Toggle the active status of an address."""
        return self.filter(pk=address_id).update(active=active)

    def update_address(self, address_id, **kwargs):
        """Update an existing address."""
        return self.filter(pk=address_id).update(**kwargs)

    def delete_address(self, address_id):
        """Delete an address."""
        return self.filter(pk=address_id).delete()

    def address_summary(self):
        """Generate a summary of addresses."""
        return self.get_queryset().address_summary()

    def increment_floor_numbers(self):
        """Increment floor numbers for addresses."""
        return self.get_queryset().increment_floor_numbers()
