from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from utility.upload_to_filename import maker
from functools import partial
from apps.account import managers
from apps.core import mixin, managers as soft_delete_manager
from django.utils.translation import gettext_lazy as _


class User(mixin.TimestampsStatusFlagMixin, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing users in the system.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags,
    AbstractBaseUser for a custom user model, and PermissionsMixin for permissions.
    """

    """
    Choices for gender
    """
    STATUS_GENDER = (
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('Other', _('Other'))
    )

    """
    Fields for user information
    """
    username = models.CharField(
        max_length=100, unique=True,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9_.+-]+$', 'Username can contain letters, numbers, underscores, dots, '
                                   'hyphens, and be at least 4 characters long.'
        )]
    )
    email = models.EmailField(
        max_length=100, unique=True,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9._%+-]+@(?:gmail|yahoo)\.com$',
            'Please enter a valid Gmail or Yahoo email address.'
        )]
    )
    phone_number = models.CharField(
        max_length=11, unique=True,
        validators=[validators.RegexValidator(
            r"09(1[0-9]|3[0-9]|2[0-9]|0[1-9]|9[0-9])[0-9]{7}$",
            'Please enter a valid phone number.'
        )]
    )
    name = models.CharField(
        max_length=50,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid name.'
        )]
    )
    last_name = models.CharField(
        max_length=50,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid last name.'
        )]
    )
    gender = models.CharField(
        max_length=10, choices=STATUS_GENDER, default='Other', blank=True, null=True,
        validators=[validators.RegexValidator(
            r'^(Male|Female|Other)$',
            message='Enter a valid gender (Male, Female, Other).'
        )]
    )
    age = models.PositiveSmallIntegerField(default=0)
    profile_picture = models.ImageField(
        upload_to=partial(maker, "profile_picture/%Y/%m/", keys=["name"]),
        max_length=255, blank=True, null=True,
        validators=[validators.FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'],
            message='Only JPG, JPEG, and PNG files are allowed.'
        )]
    )

    """
    Boolean fields for user permissions and status
    """
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    """
    Specify the field to be used as the unique identifier for the user
    """
    USERNAME_FIELD = "phone_number"

    """
    Fields required when creating a user
    """
    REQUIRED_FIELDS = ['username', 'email']

    """
    Custom managers
    """
    objects = managers.UserManager()  # Default manager
    soft_delete = soft_delete_manager.DeleteManager()  # Manager for soft deletes

    def __str__(self):
        """
        String representation of the user object
        """
        return f'{self.username} - {self.phone_number}'

    class Meta:
        """
        Meta information about the model
        """
        ordering = ('-update_time', '-create_time', 'is_deleted')
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'], name='unique_username_email')
        ]
        indexes = [
            models.Index(fields=['username', 'email', 'phone_number'], name='index_username_email')
        ]


class Address(mixin.TimestampsStatusFlagMixin):
    """
    Model representing user addresses.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags.
    """

    """
    Choices for country and city
    """
    CHOICE_COUNTRY = (
        ('Iran', _('Iran')),
    )
    CHOICE_CITY = (
        ('Tehran', _('Tehran')),
        ('Shiraz', _('Shiraz')),
        ('Mashhad', _('Mashhad')),
        ('Tabriz', _('Tabriz')),
        ('Isfahan', _('Isfahan')),
        ('Kish', _('Kish')),
        ('Kerman', _('Kerman')),
        ('Zahedan', _('Zahedan')),
        ('Fars', _('Fars')),
        ('Semnan', _('Semnan')),
        ('Yazd', _('Yazd')),
        ('Qom', _('Qom')),
        ('Ahvaz', _('Ahvaz')),
        ('Gilan', _('Gilan')),
        ('Khorasan', _('Khorasan')),
        ('Kermanshah', _('Kermanshah')),
        ('Kohgiluyeh and BoyerAhmad', _('Kohgiluyeh and BoyerAhmad')),
        ('Lorestan', _('Lorestan')),
        ('Mazandaran', _('Mazandaran')),
        ('Markazi', _('Markazi')),
        ('Hormozgan', _('Hormozgan')),
        ('Hamadan', _('Hamadan')),
        ('Ardabil', _('Ardabil')),
        ('Zanjan', _('Zanjan')),
        ('Qazvin', _('Qazvin')),
        ('Kurdistan', _('Kurdistan')),
    )

    """
    Fields for address information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='user_address')
    address_name = models.CharField(
        max_length=50,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid address name.'
        )]
    )
    country = models.CharField(
        max_length=100,
        choices=CHOICE_COUNTRY,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid country name.'
        )]
    )
    city = models.CharField(
        max_length=100,
        choices=CHOICE_CITY,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
            message='Enter a valid city name.'
        )]
    )
    street = models.CharField(
        max_length=200,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9\s.,#-]+$',
            message='Enter a valid street address.'
        )]
    )
    building_number = models.CharField(
        max_length=20,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9\s-]+$',
            message='Enter a valid building number.'
        )]
    )
    floor_number = models.CharField(
        max_length=20,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9\s-]+$',
            message='Enter a valid floor number.'
        )]
    )
    postal_code = models.CharField(
        max_length=20,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9\s-]+$',
            message='Enter a valid postal code.'
        )]
    )
    notes = models.TextField(
        blank=True, null=True,
        validators=[validators.RegexValidator(
            r'^[a-zA-Z0-9\s.,#-]+$',
            message='Enter a valid notes.'
        )]
    )
    objects = managers.AddressManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        String representation of the address object
        """
        return f'{self.user} - {self.address_name}'

    class Meta:
        """
        Meta information about the model
        """
        ordering = ('-update_time', '-create_time')
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        constraints = [
            models.UniqueConstraint(fields=['user', 'address_name'], name='unique_user_address_name')
        ]
        indexes = [
            models.Index(fields=['user', 'address_name'], name='index_user_postal_code')
        ]
