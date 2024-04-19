from django.contrib import admin
from apps.order.models import Order, OrderItem, StatusOrder, OrderPayment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for the Order model."""

    list_display = ('user', 'order_items', 'address', 'status', 'create_time', 'update_time', 'is_active', 'is_deleted')
    list_filter = ('user__username', 'status')
    search_fields = ('status', 'user__username')
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    ordering = ['-create_time']
    date_hierarchy = 'create_time'
    list_per_page = 30
    raw_id_fields = ('user',)
    fieldsets = (
        ('Creation Order', {
            'fields': ('user', 'order_items', 'address', 'status')
        }),
        ('Data', {'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
                  }),
    )
    add_fieldsets = (
        ('Creation Order', {
            'classes': ('wide',),
            'fields': ('user', 'order_items', 'address', 'status')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for the OrderItem model."""

    list_display = (
        'user', 'product', 'total_price', 'quantity', 'is_active', 'is_deleted'
    )
    list_filter = ('product__name',)
    search_fields = ('order__user__username', 'product__name', 'total_price')
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    ordering = ['-create_time']
    date_hierarchy = 'create_time'
    list_per_page = 30
    raw_id_fields = ('user', 'product')
    fieldsets = (
        ('Creation Order Item', {
            'fields': ('user', 'product', 'total_price', 'quantity')
        }),
        ('Data', {'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')}),
    )
    add_fieldsets = (
        ('Creation OrderItem', {
            'classes': ('wide',),
            'fields': ('user', 'product', 'total_price', 'quantity')
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


@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    """Admin configuration for the StatusOrder model."""

    list_display = ('user', 'order',
                    'time_accepted_order', 'accepted_order', 'time_shipped_order', 'shipped_order',
                    'time_deliver_order', 'deliver_order', 'time_rejected_order', 'rejected_order',
                    'time_cancelled_order', 'cancelled_order',)
    list_filter = (
        'user', 'order', 'accepted_order', 'shipped_order', 'deliver_order', 'rejected_order', 'cancelled_order',)
    search_fields = ('user', 'order',)
    readonly_fields = (
        'time_accepted_order', 'time_shipped_order', 'time_deliver_order', 'time_rejected_order',
        'time_cancelled_order')
    ordering = ['-time_accepted_order']
    raw_id_fields = ('user',)
    date_hierarchy = 'time_accepted_order'
    list_per_page = 30
    fieldsets = (
        ('Creation StatusOrder', {
            'fields': ('user', 'order', 'accepted_order', 'shipped_order', 'deliver_order', 'rejected_order',
                       'cancelled_order',)
        }),
        ('Data', {'fields': ('time_accepted_order', 'time_shipped_order', 'time_deliver_order',
                             'time_rejected_order', 'time_cancelled_order')
                  }),
    )
    add_fieldsets = (
        ('Creation StatusOrder', {
            'classes': ('wide',),
            'fields': ('order', 'accepted_order', 'shipped_order', 'deliver_order', 'rejected_order',
                       'cancelled_order',)
        }),
    )
