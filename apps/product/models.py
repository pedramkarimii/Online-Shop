from functools import partial
from apps.order.models import Order
from utility.upload_to_filename import maker
from django.db import models
from django.core import validators
from apps.product import managers
from apps.core import managers as delete_managers
from apps.account.models import User
from django.utils.translation import gettext_lazy as _
from apps.core import mixin, managers as soft_delete_manager


class Brand(mixin.TimestampsStatusFlagMixin):
    """
    Model to represent brands.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_brand')
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=partial(maker, "brand_logo/%Y/%m/", keys=["name"]))

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
        ordering = ['name']
        verbose_name_plural = 'Brands'
        verbose_name = 'Brand'
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='unique_name_user'),
        ]


class Media(mixin.TimestampsStatusFlagMixin):
    """
    Model to represent media associated with products.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='media_products')
    product_picture = models.ImageField(
        upload_to=partial(maker, "media_picture/%Y/%m/", keys=["product"]), max_length=255, blank=True,
        null=True, validators=[validators.FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])

    objects = managers.MediaManager()
    soft_delete = soft_delete_manager.DeleteManager()

    class Meta:
        """
        Meta options for the Media model:
        - verbose_name_plural: Plural name for the model.
        - verbose_name: Singular name for the model.
        """
        verbose_name_plural = 'Media'
        verbose_name = 'Media'


class Category(mixin.TimestampsStatusFlagMixin):
    """
    Model to represent product categories.
    """

    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, related_name='pcategory', null=True,
                                        blank=True)
    category_picture = models.ImageField(
        upload_to=partial(maker, "media_picture/%Y/%m/", keys=["name"]), max_length=255, blank=True,
        null=True, validators=[validators.FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
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


class Product(mixin.TimestampsStatusFlagMixin):
    """
    Model to represent products.
    """
    SIZE_CHOICES = [
        ('S', _('Small')),
        ('M', _('Medium')),
        ('L', _('Large')),
        ('XL', _('Extra Large')),
        ('XXL', _('Extra Extra Large')),
        ('XXXL', _('Extra Extra Extra Large')),
        ('XXXXL', _('Extra Extra Extra Extra Large')),
    ]
    COLOR_CHOICES = [
        ('RED', _('Red')),
        ('GREEN', _('Green')),
        ('BLUE', _('Blue')),
        ('YELLOW', _('Yellow')),
        ('PURPLE', _('Purple')),
        ('ORANGE', _('Orange')),
        ('BLACK', _('Black')),
        ('WHITE', _('White')),
        ('GRAY', _('Gray')),
        ('BROWN', _('Brown')),
        ('PINK', _('Pink')),
        ('GOLD', _('Gold')),
        ('SILVER', _('Silver')),
        ('BLACK', _('Black')),
    ]
    MATERIAL_CHOICES = [
        ('WOOD', _('Wood')),
        ('METAL', _('Metal')),
        ('PLASTIC', _('Plastic')),
        ('GLASS', _('Glass')),
        ('FIBER', _('Fiber')),
        ('LEATHER', _('Leather')),
        ('TEXTILE', _('Textile')),
        ('RUBBER', _('Rubber')),
        ('OTHER', _('Other')),
    ]
    WARRANTY_CHOICES = [
        ('1', _('1 Year')),
        ('2', _('2 Years')),
        ('3', _('3 Years')),
        ('4', _('4 Years')),
        ('5', _('5 Years')),
    ]

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_products')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_products')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='brand_products')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.PositiveIntegerField(validators=[validators.MinValueValidator(0)], null=True, blank=True)
    size = models.CharField(max_length=30, choices=SIZE_CHOICES, validators=[
        validators.RegexValidator(regex=r'^(S|M|L|XL|XXL|XXXL|XXXXL)$',
                                  message='Invalid size. Please select a valid size.')], null=True, blank=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, validators=[validators.RegexValidator(
        regex=r'^(RED|GREEN|BLUE|YELLOW|PURPLE|ORANGE|BLACK|WHITE|GRAY|BROWN|PINK|GOLD|SILVER|BLACK)$',
        message='Invalid color. Please select a valid color.')], null=True, blank=True)
    material = models.CharField(max_length=100, choices=MATERIAL_CHOICES, validators=[
        validators.RegexValidator(regex=r'^(WOOD|METAL|PLASTIC|GLASS|FIBER|LEATHER|TEXTILE|RUBBER|OTHER)$',
                                  message='Invalid material. Please select a valid material.')], null=True, blank=True)
    weight = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    warranty = models.CharField(max_length=20, choices=WARRANTY_CHOICES, validators=[validators.RegexValidator(
        regex=r'^(1|2|3|4|5)$', message='Invalid warranty. Please select a valid warranty.')], null=True, blank=True)
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
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='unique_product')
        ]
        indexes = [
            models.Index(fields=['name', 'category', 'brand'], name='indexes_product')
        ]


class Comment(mixin.TimestampsStatusFlagMixin):
    """
    Model to represent comments.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comments', blank=True,
                              null=True)
    is_reply = models.BooleanField(default=False)
    comment = models.TextField(max_length=500)
    objects = managers.CommentManager()
    soft_delete = soft_delete_manager.DeleteManager()

    def __str__(self):
        """
        Method to return a string representation of the Comment object.
        """
        return f'{self.user.name} - {self.comment} - {self.product.name} '

    class Meta:
        """
        Meta options for the Comment model:
        - ordering: Default ordering of query results.
        - verbose_name: Singular name for the model.
        - verbose_name_plural: Plural name for the model.
        - constraints: Database constraints.
        - indexes: Database indexes.
        """
        ordering = ['user']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_comment')
        ]
        indexes = [
            models.Index(fields=['user', 'product'], name='indexes_comment')
        ]


class CodeDiscount(mixin.TimestampsStatusFlagMixin):
    """Model representing a discount code associated with a product or category."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_code_discounts', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_code_discounts', null=True,
                              blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_code_discounts', null=True,
                                blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_code_discounts', null=True,
                                 blank=True)
    code = models.CharField(max_length=100)
    percentage_discount = models.IntegerField(null=True, blank=True,
                                              validators=[validators.MinValueValidator(0)])
    numerical_discount = models.IntegerField(null=True, blank=True,
                                             validators=[validators.MinValueValidator(0)])
    expiration_date = models.DateTimeField(null=True, blank=True)
    is_use = models.SmallIntegerField(default=0)
    is_expired = models.BooleanField(default=False)

    objects = managers.CodeDiscountManager()
    soft_delete = delete_managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the CodeDiscount."""
        return (f'{self.code} - %{self.percentage_discount} - ${self.numerical_discount} -'
                f' {self.expiration_date} - {self.is_expired}')

    class Meta:
        """Additional metadata about the CodeDiscount model."""
        ordering = ['-code']
        verbose_name = 'Code Discount'
        verbose_name_plural = 'Code Discounts'
        constraints = [
            models.UniqueConstraint(fields=['code'], name='unique_code')
        ]
        indexes = [
            models.Index(fields=['code']),
        ]


class WarehouseKeeper(mixin.TimestampsStatusFlagMixin):
    """Model representing a user responsible for managing inventory in a warehouse."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_warehouse_keepers')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_warehouse_keepers')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_warehouse_keepers')
    quantity = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=True)

    objects = managers.WarehouseKeeperManager()
    soft_delete = delete_managers.DeleteManager()

    def __str__(self):
        """Return a string representation of the WarehouseKeeper."""
        return f'{self.user} - {self.product} - {self.quantity}'

    class Meta:
        """Additional metadata about the WarehouseKeeper model."""
        ordering = ['-user', '-product']
        verbose_name = 'Warehouse Keeper'
        verbose_name_plural = 'Warehouse Keepers'
        indexes = [
            models.Index(fields=['user', 'product']),
        ]
