from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.core import validators
from apps.core.upload_to_filename import maker
from functools import partial
from apps.account import managers
from apps.core.mixin import mixin_model
from apps.core import managers as soft_delete_manager
from django.utils.translation import gettext_lazy as _


class Role(mixin_model.TimestampsStatusFlagMixin):
    """
    Model representing a role.
    """
    code_discount = models.ForeignKey(
        'CodeDiscount', on_delete=models.CASCADE, verbose_name=_('Discount Code'))
    golden = models.ForeignKey(
        'User', on_delete=models.CASCADE, blank=True, null=True, related_name='golden_roles',
        verbose_name=_('Golden')
    )
    silver = models.ForeignKey(
        'User', on_delete=models.CASCADE, blank=True, null=True, related_name='silver_roles',
        verbose_name=_('Silver')
    )
    bronze = models.ForeignKey(
        'User', on_delete=models.CASCADE, blank=True, null=True, related_name='bronze_roles',
        verbose_name=_('Bronze')
    )
    seller = models.ForeignKey(
        'User', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Seller')
    )
    objects = managers.RoleManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        return f"{self.golden} - {self.silver} - {self.bronze} - {self.seller}"

    class Meta:
        """
        Meta information about the model
        """
        ordering = ('-update_time', '-create_time')
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        constraints = [
            models.UniqueConstraint(fields=['golden'], name='unique_golden'),
            models.UniqueConstraint(fields=['silver'], name='unique_silver'),
            models.UniqueConstraint(fields=['bronze'], name='unique_bronze'),
            models.UniqueConstraint(fields=['seller'], name='unique_seller'),
        ]
        indexes = [
            models.Index(fields=['golden', 'silver', 'bronze'], name='golden_silver_bronze_index')
        ]


class User(mixin_model.TimestampsStatusFlagMixin, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing users in the system.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags,
    AbstractBaseUser for a custom user model, and PermissionsMixin for permissions.
    """

    """
    Fields for user information
    """
    username = models.CharField(
        max_length=100, unique=True,
        validators=[validators.UsernameValidator()], verbose_name=_('Username')
    )
    email = models.EmailField(
        max_length=100, unique=True,
        validators=[validators.EmailValidator()], verbose_name=_('Email')
    )
    phone_number = models.CharField(
        max_length=11, unique=True,
        validators=[validators.PhoneNumberMobileValidator()], verbose_name=_('Phone Number')
    )

    """
    Boolean fields for user permissions and status
    """
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
    objects = managers.UserManager()
    soft_delete = soft_delete_manager.DeleteManager()

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


class UserAuth(mixin_model.TimestampsStatusFlagMixin):
    """
    Model representing user authentication tokens.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags.
    """
    ACCESS_TOKEN = 1
    REFRESH_TOKEN = 2

    TOKEN_TYPE_CHOICES = (
        (ACCESS_TOKEN, "access token"),
        (REFRESH_TOKEN, "refresh token")
    )
    user_id = models.IntegerField(verbose_name=_("user id"), )
    token_type = models.PositiveSmallIntegerField(choices=TOKEN_TYPE_CHOICES,
                                                  verbose_name=_("token type"))
    uuid = models.UUIDField(verbose_name=_("uuid"), unique=True)

    objects = managers.UserAuthManager()

    class Meta:
        verbose_name = _("UserAuth")
        verbose_name_plural = _("UserAuths")
        ordering = ("-id",)
        indexes = [
            models.Index(fields=["user_id"], name="user_id_index"),
        ]

    def __str__(self):
        return f"user id: {self.user_id} - token type(a = 1, r = 2): {self.token_type} - {self.uuid}"


class Profile(mixin_model.TimestampsStatusFlagMixin):
    """
    Model representing user profiles.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(
        max_length=50,
        validators=[validators.NameValidator()], verbose_name=_('Name')
    )
    last_name = models.CharField(
        max_length=50,
        validators=[validators.LastNameValidator()], verbose_name=_('Last Name')
    )
    gender = models.CharField(
        max_length=10, choices=validators.GenderChoices.CHOICES, default='Other',
        validators=[validators.GenderValidator()], verbose_name=_('Gender')
    )
    age = models.PositiveSmallIntegerField(default=0, verbose_name=_('Age'))
    profile_picture = models.ImageField(
        upload_to=partial(maker, "profile_picture/%Y/%m/", keys=["name"]),
        max_length=255, blank=True, null=True,
        validators=[validators.PictureValidator()], verbose_name=_('Profile Picture')
    )
    objects = managers.ProfileManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        String representation of the profile object
        """
        return f'{self.user} - {self.name} {self.last_name}'

    class Meta:
        """
        Meta information about the model
        """
        ordering = ('-update_time', '-create_time')
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        indexes = [
            models.Index(fields=['user'], name='index_user_profile')
        ]


class Address(mixin_model.TimestampsStatusFlagMixin):
    """
    Model representing user addresses.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags.
    """

    """
    Fields for address information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='user_address')
    address_name = models.CharField(
        max_length=50,
        validators=[validators.NameValidator()], verbose_name=_('Address Name')
    )
    country = models.CharField(
        max_length=100,
        choices=validators.CountryChoices.CHOICES,
        validators=[validators.CountryValidator()], verbose_name=_('Country')
    )
    city = models.CharField(
        max_length=100,
        choices=validators.CityChoices.CHOICES,
        validators=[validators.CityValidator()], verbose_name=_('City')
    )
    street = models.CharField(
        max_length=200,
        validators=[validators.StreetValidator()], verbose_name=_('Street')
    )
    building_number = models.CharField(
        max_length=20,
        validators=[validators.BuildingNumberValidator()], verbose_name=_('Building Number')
    )
    floor_number = models.IntegerField(
        default=0, verbose_name=_('Floor Number')
    )
    postal_code = models.PositiveSmallIntegerField(
        default=0, verbose_name=_('Postal Code')
    )
    notes = models.TextField(
        blank=True, null=True,
        validators=[validators.NotesValidator()], verbose_name=_('Notes')
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


class CodeDiscount(mixin_model.TimestampsStatusFlagMixin):
    """
    Model representing discount codes.
    Inherits from mixin.TimestampsStatusFlagMixin for timestamps and status flags.
    """

    """
    Fields for discount code information
    """

    role_name = models.CharField(max_length=100, choices=validators.RoleChoices.CHOICES, verbose_name=_('Role Name'))
    code = models.CharField(
        max_length=100,
        validators=[validators.CodeValidator()], verbose_name=_('Code')
    )
    percentage_discount = models.SmallIntegerField(null=True, blank=True,
                                                   choices=validators.PercentDiscountChoices.CHOICES,
                                                   validators=[validators.PercentageDiscountValidator()],
                                                   verbose_name=_('Percentage Discount'))
    numerical_discount = models.SmallIntegerField(null=True, blank=True,
                                                  validators=[validators.NumericalDiscountValidator()],
                                                  verbose_name=_('Numerical Discount'))
    expiration_date = models.DateField(null=True, blank=True, verbose_name=_('Expiration Date'))
    is_use = models.SmallIntegerField(default=1, choices=validators.IsUseChoice.CHOICES)
    is_expired = models.BooleanField(default=False)
    objects = managers.CodeDiscountManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        String representation of the discount code object
        """
        return (f' {self.role_name} - {self.code} - % {self.percentage_discount}'
                f'- $ {self.numerical_discount} - {self.expiration_date}')

    class Meta:
        """
        Meta information about the model
        """
        ordering = ('-update_time', '-create_time')
        verbose_name = 'discount code'
        verbose_name_plural = 'discount codes'
        constraints = [
            models.UniqueConstraint(fields=('code', 'role_name'), name='unique_code_discount_role_name')
        ]
        indexes = [
            models.Index(fields=['code'], name='index_code')
        ]
