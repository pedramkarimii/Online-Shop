from django.contrib import admin
from apps.order.models import Order, OrderItem, OrderPayment


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for the OrderItem model."""

    list_display = (
        'user', 'product', 'total_price', 'quantity', 'is_active', 'is_deleted'
    )
    list_filter = ('user__username', 'product__name', 'total_price')
    search_fields = ('ser__username', 'product__name', 'total_price')
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    ordering = ('-create_time',)
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for the Order model."""

    list_display = (
        'address', 'display_order_items', 'status', 'transaction_id', 'payment_method', 'finally_price',
        'time_accepted_order', 'accepted_order', 'time_shipped_order', 'shipped_order', 'time_deliver_order',
        'deliver_order', 'time_rejected_order', 'rejected_order', 'time_cancelled_order', 'cancelled_order',
        'create_time', 'update_time', 'is_active', 'is_deleted')
    list_filter = ('status', 'address__user__username', 'payment_method', 'time_accepted_order')
    search_fields = ('status', 'address__user__username', 'payment_method', 'time_accepted_order')
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    ordering = ('-create_time',)
    date_hierarchy = 'create_time'
    list_per_page = 30
    raw_id_fields = ('address',)
    fieldsets = (
        ('Creation Order', {
            'fields': (
                'address', 'order_item', 'status', 'transaction_id', 'payment_method',
                'finally_price',
                'time_accepted_order', 'time_shipped_order', 'time_deliver_order',
                'time_rejected_order', 'time_cancelled_order')
        }),
        ('Data', {'fields': ('accepted_order',
                             'shipped_order',
                             'deliver_order',
                             'rejected_order',
                             'cancelled_order',
                             'create_time', 'update_time', 'is_active', 'is_deleted')
                  }),
    )
    add_fieldsets = (
        ('Creation Order', {
            'classes': ('wide',),
            'fields': (
                'address', 'order_item', 'status', 'transaction_id', 'payment_method',
                'finally_price',
                'time_accepted_order', 'time_shipped_order', 'time_deliver_order',
                'time_rejected_order', 'time_cancelled_order')
        }),
    )

    def display_order_items(self, obj):
        """Custom method to display order items."""
        return ", ".join(
            [f"{item.product.name} (Qty: {item.quantity}, Total: {item.total_price})" for item in obj.order_item.all()]
        )

    display_order_items.short_description = 'Order Items'


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for OrderPayment model.
    """

    list_display = (
        'transaction_payment', 'order', 'amount', 'cardholder_name', 'card_number', 'expiration_date', 'cvv', 'status', 'payment_time',
        'is_paid', 'is_failed', 'is_canceled'
    )
    list_filter = (
        'transaction_payment', 'order__address__user__username', 'amount', 'status', 'is_paid', 'is_failed', 'is_canceled'
    )
    search_fields = ('transaction_payment', 'order__address__user__username', 'status')
    readonly_fields = ('transaction_payment', 'payment_time', 'is_failed', 'is_canceled', 'is_paid')
    ordering = ('-payment_time',)
    date_hierarchy = 'payment_time'
    list_per_page = 30
    raw_id_fields = ('order',)
    fieldsets = (
        ('Creation Order Payment', {
            'fields': (
                'order', 'amount', 'cardholder_name', 'card_number', 'expiration_date', 'cvv',
                'status'
            )
        }),
        ('Data', {
            'fields': ('transaction_payment', 'payment_time', 'is_paid', 'is_failed', 'is_canceled')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'order', 'amount', 'cardholder_name', 'card_number', 'expiration_date', 'cvv', 'status', 'payment_time'
            )
        }),
    )
