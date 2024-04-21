from django.contrib import admin
from apps.product.models import Product, Comment, Brand, Category, Media, WarehouseKeeper, Discount, FavoritesBasket


class MediaInline(admin.StackedInline):
    model = Media
    can_delete = False
    verbose_name_plural = 'Media'
    fk_name = 'product'
    ordering = ('-create_time', '-update_time')
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    fieldsets = (
        ('Creation Media', {
            'fields': ('product', 'product_picture',)
        }),
        ('Data', {
            'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product__name', 'product_picture',)
        }),
    )


class DiscountInline(admin.StackedInline):
    model = Discount
    can_delete = False
    verbose_name_plural = 'Code Discounts'
    fk_name = 'product'
    ordering = ('-create_time', '-update_time')
    readonly_fields = ('is_use', 'is_deleted', 'is_active', 'expiration_date', 'create_time', 'update_time')
    fieldsets = (
        ('Creation Code discount', {
            'fields': ('product', 'category', 'percentage_discount', 'numerical_discount',
                       'expiration_date')
        }),
        ('Data', {
            'fields': ('is_use', 'is_deleted', 'is_active', 'create_time', 'update_time')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product', 'category', 'percentage_discount', 'numerical_discount', 'is_use',
                       'is_deleted', 'is_active', 'expiration_date')
        }),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for the Brand model."""

    list_display = ('user', 'name', 'description', 'location', 'is_active', 'is_deleted')
    search_fields = ('user__username', 'name', 'description', 'location')
    list_filter = ('user__username', 'name', 'description', 'location', 'is_active')
    ordering = ('-create_time', '-update_time')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    fieldsets = (
        ('Creation Brand', {
            'fields': ('user', 'name', 'description', 'location')
        }),
        ('Data', {
            'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'name', 'description', 'location', 'is_active')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""

    list_display = ('name', 'parent_category', 'is_sub_category', 'is_active', 'is_deleted')
    search_fields = ('name', 'parent_category', 'is_sub_category', 'is_active')
    ordering = ('-create_time', '-update_time')
    list_filter = ('name', 'parent_category', 'is_sub_category', 'is_active')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    fieldsets = (
        ('Creation Category ', {
            'fields': ('name', 'parent_category', 'is_sub_category', 'category_picture')
        }),
        ('Data', {
            'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'parent_category', 'is_sub_category', 'is_active', 'category_picture')
        }),
    )


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Admin configuration for the Media model."""

    list_display = ('product', 'product_picture', 'create_time', 'update_time', 'is_active', 'is_deleted')
    search_fields = ('product__name', 'product_picture',)
    ordering = ('-create_time', '-update_time', 'create_time')
    list_filter = ('product__name', 'is_active', 'is_deleted')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    fieldsets = (
        ('Creation Media', {
            'fields': ('product', 'product_picture',)
        }),
        ('Data', {
            'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product__name', 'product_picture',)
        }),
    )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Discount model.
    """

    list_display = (
        'product', 'category', 'percentage_discount', 'numerical_discount',
        'expiration_date', 'is_use', 'is_expired', 'is_active', 'is_deleted',
    )
    search_fields = ('product__name', 'category__name', 'percentage_discount',
                     'numerical_discount',)
    list_filter = ('product__name', 'category__name', 'percentage_discount',
                   'numerical_discount', 'expiration_date', 'is_expired', 'is_active')
    ordering = ('-create_time', '-update_time')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('is_use', 'is_deleted', 'is_active', 'create_time', 'update_time')
    fieldsets = (
        ('Creation Code discount', {
            'fields': ('product', 'category', 'percentage_discount', 'numerical_discount',
                       'expiration_date')
        }),
        ('Data', {
            'fields': ('is_use', 'is_deleted', 'is_active', 'create_time', 'update_time')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product', 'category', 'percentage_discount', 'numerical_discount', 'is_use',
                       'is_deleted', 'is_active', 'expiration_date')
        }),
    )


@admin.register(WarehouseKeeper)
class WarehouseKeeperAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for WarehouseKeeper model.
    """

    list_display = (
        'user', 'brand', 'product', 'quantity', 'create_time', 'update_time', 'is_deleted', 'is_active'
    )
    search_fields = (
        'user__username', 'brand__name', 'product__name', 'quantity', 'create_time', 'update_time'
    )
    ordering = ('-create_time', '-update_time')
    list_filter = (
        'user__username', 'brand__name', 'product__name', 'quantity', 'create_time', 'update_time'
    )
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('create_time', 'update_time', 'is_deleted', 'is_active')
    fieldsets = (
        ('Creation Warehouse Keeper', {
            'fields': ('user', 'brand', 'product', 'quantity')
        }),
        ('Data', {
            'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user__username', 'brand', 'product', 'quantity')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment', 'reply', 'is_reply')
    search_fields = ('user__username', 'product__name', 'reply', 'is_reply', 'comment')
    ordering = ('-create_time', '-update_time')
    list_filter = ('user__username', 'product__name', 'reply', 'is_reply', 'comment')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('create_time', 'update_time')
    fieldsets = (
        ('Creation Comment', {
            'fields': ('user', 'product', 'reply', 'is_reply', 'comment')
        }),
        ('Data', {
            'fields': ('create_time', 'update_time')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'product', 'reply', 'is_reply', 'comment')
        }),
    )


@admin.register(FavoritesBasket)
class FavoritesBasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'available', 'quantity')
    search_fields = ('user__username', 'product__name', 'available', 'quantity')
    ordering = ('-create_time', '-update_time')
    list_filter = ('user__username', 'product__name', 'available', 'quantity')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('available', 'create_time', 'update_time')
    fieldsets = (
        ('Creation Favorites Basket', {
            'fields': ('user', 'product', 'quantity')
        }),
        ('Data', {
            'fields': ('available', 'create_time', 'update_time')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user__username', 'product__name', 'available', 'quantity')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    list_display = (
        'name', 'brand', 'category', 'description', 'price', 'size', 'color', 'material', 'weight',
        'height',
        'width', 'warranty', 'quantity', 'is_active', 'is_deleted'
    )
    search_fields = (
        'brand__name', 'name', 'brand__name', 'category__name', 'description', 'price', 'size', 'color',
        'material', 'weight', 'height', 'width', 'warranty', 'quantity'
    )
    date_hierarchy = 'create_time'
    list_per_page = 30
    ordering = ('-create_time', '-update_time')
    list_filter = (
        'name', 'brand__name', 'category__name', 'size', 'color', 'material', 'is_active', 'is_deleted'
    )

    fieldsets = (
        ('Creation Product', {
            'fields': (
                'name', 'brand', 'category', 'description', 'price', 'size', 'color', 'material', 'weight',
                'height', 'width', 'warranty', 'quantity'
            )
        }),
        ('Data', {
            'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'brand', 'category', 'description', 'price', 'size', 'color', 'material', 'weight',
                'height', 'width', 'warranty', 'quantity', 'is_active', 'is_deleted'
            )
        }),
    )
    inlines = (MediaInline,)

    def get_inline_instances(self, request, obj=None):
        """Get inline instances based on whether an object is provided."""
        if not obj:
            return list()
        return super(ProductAdmin, self).get_inline_instances(request, obj)
