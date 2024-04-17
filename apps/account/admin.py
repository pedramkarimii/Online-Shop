from django.contrib import admin
from apps.account.models import User, Address
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class AddressInline(admin.StackedInline):
    """Inline for managing addresses within the user admin."""

    model = Address
    can_delete = False
    verbose_name_plural = 'Address'
    fk_name = 'user'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin interface for managing addresses."""

    list_display = ['user', 'address_name', 'country', 'city',
                    'street', 'is_deleted', 'is_active']
    list_filter = ['user', 'address_name', 'country']
    search_fields = ['user', 'address_name', 'country']
    readonly_fields = ('create_time', 'update_time', 'is_deleted', 'is_active')
    ordering = ['-city']
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Address', {'fields': ('user', 'address_name', 'country',
                                         'city', 'street', 'building_number', 'floor_number', 'postal_code', 'notes')}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  }),
    )
    add_fieldsets = (
        ('Creation Address', {
            'classes': ('wide',),
            'fields': ('user', 'address_name', 'country',
                       'city', 'street', 'building_number', 'floor_number', 'postal_code', 'notes')
        }),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for managing users."""

    fieldsets = (
        ('Change personal info',
         {'fields': (
             'email', 'phone_number', 'username', 'name', 'last_name', 'gender', 'age', 'profile_picture',
             'password')}),
        ('Permissions',
         {'fields': ('is_admin', 'is_superuser', 'is_staff', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'create_time', 'update_time', 'is_active', 'is_deleted',)}),
    )

    add_fieldsets = (
        ('Creation User', {
            'fields': (
                'name', 'last_name', 'gender', 'age', 'email', 'phone_number', 'username', 'profile_picture',
                'password1', 'password2')}
         ),
    )
    row_id_fields = ('phone_number',)
    list_display = ('username', 'email', 'phone_number', 'is_deleted', 'is_admin', 'is_active')
    list_filter = ['username', 'email', 'phone_number', 'is_deleted', 'is_active']
    search_fields = ['username', 'email', 'phone_number']
    date_hierarchy = 'create_time'
    list_per_page = 30
    ordering = ['-username']
    readonly_fields = ('create_time', 'update_time', 'last_login', 'is_active', 'is_deleted',)
    filter_horizontal = ('groups', 'user_permissions')

    inlines = (AddressInline,)

    def get_inline_instances(self, request, obj=None):
        """Get inline instances based on whether an object is provided."""
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """Get the form for the admin interface."""
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser and 'is_superuser' in form.base_fields:
            form.base_fields["is_superuser"].disabled = True
            form.base_fields["is_admin"].disabled = True
            form.base_fields["is_staff"].disabled = True
            form.base_fields["is_active"].disabled = True
            form.base_fields["is_deleted"].disabled = True
        return form
