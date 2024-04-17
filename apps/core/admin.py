from django.contrib import admin
from apps.core.models import OrderPayment, CodeDiscount, WarehouseKeeper


@admin.register(CodeDiscount)
class CodeDiscountAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for CodeDiscount model.
    """

    list_display = (
        'code', 'percentage_discount', 'numerical_discount',
        'expiration_date', 'is_expired', 'is_active'
    )
    search_fields = ('code', 'percentage_discount', 'numerical_discount',)
    ordering = ('-create_time', '-update_time')
    list_filter = ('code', 'percentage_discount', 'numerical_discount', 'is_expired', 'is_active')
    date_hierarchy = 'create_time'
    list_per_page = 30
    readonly_fields = ('create_time', 'update_time')
    fieldsets = (
        ('Information', {
            'fields': ('code', 'percentage_discount', 'numerical_discount', 'expiration_date')
        }),
        ('Data', {
            'fields': ('create_time', 'update_time')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('code', 'percentage_discount', 'numerical_discount', 'expiration_date')
        }),
    )


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for OrderPayment model.
    """

    list_display = (
        'user', 'order', 'amount', 'cardholder_name', 'card_number', 'expiration_date', 'cvv', 'transaction_id',
        'payment_method', 'status', 'payment_time', 'is_paid', 'is_failed', 'is_canceled'
    )
    list_filter = (
        'transaction_id', 'user', 'order', 'amount', 'payment_method', 'status', 'is_paid', 'is_failed', 'is_canceled'
    )
    search_fields = ('transaction_id', 'order', 'status')
    readonly_fields = ('transaction_id', 'payment_time', 'is_failed', 'is_canceled', 'is_paid')
    ordering = ('-payment_time',)
    date_hierarchy = 'payment_time'
    list_per_page = 30
    raw_id_fields = ('order',)
    fieldsets = (
        ('Creation Order Payment', {
            'fields': (
                'user', 'order', 'amount', 'cardholder_name', 'card_number', 'expiration_date', 'cvv', 'transaction_id',
                'payment_method', 'status'
            )
        }),
        ('Data', {
            'fields': ('payment_time', 'is_paid', 'is_failed', 'is_canceled')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'user', 'order', 'amount', 'cardholder_name', 'card_number', 'expiration_date', 'cvv', 'transaction_id',
                'payment_method', 'status', 'payment_time'
            )
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
