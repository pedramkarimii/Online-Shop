from functools import partial
from apps.core.upload_to_filename import maker
from django.db import models

from apps.order.models import Order
from apps.product import managers
from apps.core import managers as delete_managers
from apps.account.models import User
from django.utils.translation import gettext_lazy as _
from apps.core.mixin import mixin_model
from apps.core import managers as soft_delete_manager
from apps.core import validators


class Brand(mixin_model.TimestampsStatusFlagMixin):
    """
    Model to represent brands.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_brand')
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    phone_number = models.CharField(max_length=11, unique=True, validators=[validators.PhoneNumberValidator()],
                                    verbose_name=_('Phone Number'))
    description = models.TextField(verbose_name=_('Description'))
    location = models.CharField(max_length=200, verbose_name=_('Location'))
    logo = models.ImageField(upload_to=partial(maker, "brand_logo/%Y/%m/", keys=["name"]), verbose_name=_('Logo'))

    objects = managers.BrandManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        Method to return a string representation of the Brand object.
        """
        return f'{self.name}'

    class Meta:
        """
        Meta options for the Brand model:
        - ordering: Default ordering of query results.
        - verbose_name_plural: Plural name for the model.
        - verbose_name: Singular name for the model.
        - indexes: Database indexes.
        - constraints: Database constraints.
        """
        ordering = ('name',)
        verbose_name_plural = 'Brands'
        verbose_name = 'Brand'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name_user'),
        ]


class Media(mixin_model.TimestampsStatusFlagMixin):
    """
    Model to represent media associated with products.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='media_products')
    product_picture = models.ImageField(
        upload_to=partial(maker, "media_picture/%Y/%m/", keys=["product"]), max_length=255, blank=True,
        null=True, validators=[validators.PictureValidator()], verbose_name=_('Product Picture'))

    objects = managers.MediaManager()
    soft_delete = soft_delete_manager.DeleteManager()

    class Meta:
        """
        Meta options for the Media model:
        - verbose_name_plural: Plural name for the model.
        - verbose_name: Singular name for the model.
        """
        ordering = ('-product',)
        verbose_name_plural = 'Media'
        verbose_name = 'Media'


class Category(mixin_model.TimestampsStatusFlagMixin):
    """
    Model to represent product categories.
    """

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, related_name='pcategory', null=True,
                                        blank=True)
    category_picture = models.ImageField(
        upload_to=partial(maker, "media_picture/%Y/%m/", keys=["name"]), max_length=255, blank=True,
        null=True, validators=[validators.PictureValidator()], verbose_name=_('Category Picture'))
    is_sub_category = models.BooleanField(default=False)

    objects = managers.CategoryManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        Method to return a string representation of the Category object.
        """
        return f'{self.name}'

    class Meta:
        """
        Meta options for the Category model:
        - ordering: Default ordering of query results.
        - verbose_name_plural: Plural name for the model.
        - verbose_name: Singular name for the model.
        - indexes: Database indexes.
        - constraints: Database constraints.
        """
        ordering = ['name']
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name'),
        ]


class Product(mixin_model.TimestampsStatusFlagMixin):
    """
    Model to represent products.
    """

    """
    Fields for product:
    - user: User who created the product.
    - name: Name of the product.
    - description: Description of the product.
    - price: Price of the product.
    - size: Size of the product.
    - color: Color of the product.
    - material: Material of the product.
    - weight: Weight of the product.
    - height: Height of the product.
    - width: Width of the product.
    - stock: Stock quantity of the product.
    - category: Relationship with the Category model.
    - brand: Relationship with the Brand model.
    - warranty: Warranty period for the product.
    """
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_products')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='brand_products')
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(max_length=500, verbose_name=_('Description'))
    price = models.PositiveIntegerField(validators=[validators.PriceValidator()], null=True, blank=True)
    size = models.CharField(max_length=30, choices=validators.SizeChoice.CHOICES, verbose_name=_('Size'),
                            validators=[validators.SizeValidator()], null=True, blank=True)
    color = models.CharField(max_length=20, choices=validators.ColorChoice.CHOICES, verbose_name=_('Color'),
                             validators=[validators.ColorValidator()], null=True, blank=True)
    material = models.CharField(max_length=100, choices=validators.MaterialChoice.CHOICES, verbose_name=_('Material'),
                                validators=[validators.MaterialValidator()], null=True,
                                blank=True)
    weight = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    warranty = models.CharField(max_length=20, choices=validators.WarrantyChoice.CHOICES, verbose_name=_('Warranty'),
                                validators=[validators.WarrantyValidator()], null=True,
                                blank=True)
    quantity = models.PositiveSmallIntegerField(default=0)

    objects = managers.ProductManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        Method to return a string representation of the Product object.
        """
        return f'{self.name} - {self.price} - {self.category.name} - {self.brand.name}'

    class Meta:
        """
        Meta options for the Product model:
        - ordering: Default ordering of query results.
        - verbose_name: Singular name for the model.
        - verbose_name_plural: Plural name for the model.
        - constraints: Database constraints.
        - indexes: Database indexes.
        """
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='unique_product')
        ]
        indexes = [
            models.Index(fields=['name', 'category', 'brand'], name='indexes_product')
        ]


class Comment(mixin_model.TimestampsStatusFlagMixin):
    """
    Model to represent comments.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comments', blank=True,
                              null=True)
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=500, verbose_name=_('Comment'))
    objects = managers.CommentManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        Method to return a string representation of the Comment object.
        """
        return f'{self.comment} - {self.product.name} '

    class Meta:
        """
        Meta options for the Comment model:
        - ordering: Default ordering of query results.
        - verbose_name: Singular name for the model.
        - verbose_name_plural: Plural name for the model.
        - constraints: Database constraints.
        - indexes: Database indexes.
        """
        ordering = ('-create_time',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['user', 'product'], name='indexes_comment')
        ]


class Wishlist(mixin_model.TimestampsStatusFlagMixin):
    """Model representing a user's favorite or basket products."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlist')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_wishlist', null=True,
                              blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)

    objects = managers.WishlistManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """Return a string representation of the Wishlist."""
        return f'{self.user} - {self.product} - {self.quantity}'

    class Meta:
        """Additional metadata about the Wishlist model."""
        ordering = ('user',)
        verbose_name = 'Favorites Basket'
        verbose_name_plural = 'Favorites Baskets'
        indexes = [
            models.Index(fields=['user', 'product']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user')
        ]


class Discount(mixin_model.TimestampsStatusFlagMixin):
    """Model representing a discount code associated with a product or category."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_code_discounts', null=True,
                                blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_code_discounts', null=True,
                                 blank=True)
    percentage_discount = models.IntegerField(null=True, blank=True, choices=validators.PercentDiscountChoices.CHOICES,
                                              validators=[validators.PercentageDiscountValidator()])
    numerical_discount = models.IntegerField(null=True, blank=True,
                                             validators=[validators.NumericalDiscountValidator()])
    expiration_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Expiration Date'))
    is_use = models.SmallIntegerField(default=1, choices=validators.IsUseChoice.CHOICES)
    is_expired = models.BooleanField(default=False)

    objects = managers.CodeDiscountManager()
    soft_delete = delete_managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the Discount."""
        return (f'%{self.percentage_discount} - ${self.numerical_discount} -'
                f' {self.expiration_date} - {self.is_expired}')

    class Meta:
        """Additional metadata about the Discount model."""
        ordering = ('update_time', '-create_time')
        verbose_name = 'Discount %'
        verbose_name_plural = 'Discounts %'
        indexes = [
            models.Index(fields=['product', 'category']),
        ]


class Inventory(mixin_model.TimestampsStatusFlagMixin):
    """Model representing a warehouse inventory."""
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    quantity = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.TextField(max_length=500, verbose_name=_('Description'))

    objects = managers.InventoryManager()
    soft_delete = delete_managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the Inventory."""
        return f'{self.quantity} - {self.available}'

    class Meta:
        """Additional metadata about the Inventory model."""
        ordering = ('name',)
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'


class AddToInventory(mixin_model.TimestampsStatusFlagMixin):
    """Model representing a user responsible for managing inventory in a warehouse."""
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='inventory_add_to_inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_add_to_inventory')
    quantity = models.PositiveSmallIntegerField(default=0)

    objects = managers.AddToInventoryManager()
    soft_delete = delete_managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the AddToInventory."""
        return f'{self.inventory} - {self.product} - {self.quantity}'

    class Meta:
        """Additional metadata about the AddToInventory model."""
        ordering = ('product',)
        verbose_name = 'AddToInventory'
        verbose_name_plural = 'AddToInventories'
        indexes = [
            models.Index(fields=['inventory', 'product']),
        ]
