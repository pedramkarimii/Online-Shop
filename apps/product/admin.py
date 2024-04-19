from django.contrib import admin
from apps.product.models import Product, Comment, Brand, Category, Media, WarehouseKeeper, CodeDiscount


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for the Brand model."""

    list_display = ('user', 'name', 'description', 'location', 'is_active', 'is_deleted')
    search_fields = ('user', 'name', 'description', 'location')
    ordering = ('-create_time', '-update_time')
    list_filter = ('user', 'name', 'description', 'location', 'is_active')
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
    list_filter = ('is_active', 'is_deleted')
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

    def product_name(self, obj):
        return obj.product.name if obj.product else ''

    product_name.short_description = 'Product'


@admin.register(CodeDiscount)
class CodeDiscountAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for CodeDiscount model.
    """

    list_display = (
        'user', 'order', 'product', 'category',
        'code', 'percentage_discount', 'numerical_discount',
        'expiration_date', 'is_use', 'is_expired', 'is_active', 'is_deleted',
    )
    search_fields = ('user', 'order', 'product', 'category', 'code', 'percentage_discount', 'numerical_discount',)
    ordering = ('-create_time', '-update_time')
    list_filter = (
        'user', 'order', 'product', 'category', 'code', 'percentage_discount', 'numerical_discount', 'expiration_date',
        'is_expired', 'is_active')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('is_use', 'is_deleted', 'is_active', 'expiration_date', 'create_time', 'update_time')
    fieldsets = (
        ('Creation Code discount', {
            'fields': ('user', 'order', 'product', 'category', 'code', 'percentage_discount', 'numerical_discount',
                       'expiration_date')
        }),
        ('Data', {
            'fields': ('is_use', 'is_deleted', 'is_active', 'create_time', 'update_time')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user', 'order', 'product', 'category', 'code', 'percentage_discount', 'numerical_discount', 'is_use',
                'is_deleted', 'is_active',
                'expiration_date')
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
        'user', 'brand__name', 'product__name', 'quantity', 'create_time', 'update_time'
    )
    ordering = ('-create_time', '-update_time')
    list_filter = (
        'user', 'brand__name', 'product__name', 'quantity', 'create_time', 'update_time'
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
            'fields': ('user', 'brand', 'product', 'quantity')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment', 'reply', 'is_reply')
    search_fields = ('user', 'product', 'reply', 'is_reply', 'comment')
    ordering = ('-create_time', '-update_time')
    list_filter = ('user', 'product', 'reply', 'is_reply', 'comment')
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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    list_display = (
        'user', 'name', 'brand', 'category', 'description', 'price', 'size', 'color', 'material', 'weight',
        'height',
        'width', 'warranty', 'quantity', 'is_active', 'is_deleted'
    )
    search_fields = (
        'user__username', 'name', 'brand__name', 'category__name', 'description', 'price', 'size', 'color',
        'material', 'weight', 'height', 'width', 'warranty', 'quantity'
    )
    date_hierarchy = 'create_time'
    list_per_page = 30
    ordering = ('-create_time', '-update_time')
    list_filter = (
        'user__username', 'brand__name', 'category__name', 'size', 'color', 'material', 'is_active', 'is_deleted'
    )

    fieldsets = (
        ('Creation Product', {
            'fields': (
                'user', 'name', 'brand', 'category', 'description', 'price', 'size', 'color', 'material', 'weight',
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
                'user', 'name', 'brand', 'category', 'description', 'price', 'size', 'color', 'material', 'weight',
                'height', 'width', 'warranty', 'quantity', 'is_active', 'is_deleted'
            )
        }),
    )
