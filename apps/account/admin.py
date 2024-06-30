from django.contrib import admin
from apps.account.models import User, Address, CodeDiscount, UserAuth, Profile, Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class AddressInline(admin.StackedInline):
    """Inline for managing addresses within the user admin."""

    model = Address
    can_delete = False
    verbose_name_plural = 'Address'
    fk_name = 'user'
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


class RoleInline(admin.StackedInline):
    """Inline for managing addresses within the user admin."""

    model = Role
    can_delete = False
    verbose_name_plural = 'Role'
    fk_name = 'golden'
    readonly_fields = ('code_discount', 'create_time', 'update_time', 'is_deleted', 'is_active')
    ordering = ('update_time', 'create_time')
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Address', {'fields': ('code_discount', 'golden', 'silver', 'bronze')}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  }),
    )
    add_fieldsets = (
        ('Creation Address', {
            'classes': ('wide',),
            'fields': ('code_discount', 'golden', 'silver', 'bronze')
        }),
    )


class CodeDiscountInline(admin.StackedInline):
    """Inline for managing addresses within the user admin."""

    model = CodeDiscount
    can_delete = False
    verbose_name_plural = 'CodeDiscount'
    fk_name = 'role'
    readonly_fields = ('create_time', 'update_time', 'is_deleted', 'is_active')
    ordering = ('create_time',)
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Address',
         {'fields': ('role', 'code', 'percentage_discount', 'numerical_discount', 'expiration_date', 'is_use')}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  }),
    )
    add_fieldsets = (
        ('Creation Address', {
            'classes': ('wide',),
            'fields': ('role', 'code', 'percentage_discount', 'is_active', 'is_deleted')
        }),
    )


class ProfileInline(admin.StackedInline):
    """Inline for managing profiles within the user admin."""

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ('create_time', 'update_time', 'is_deleted', 'is_active')
    ordering = ('create_time',)
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Profile', {'fields': ('user', 'name', 'last_name', 'gender', 'age', 'profile_picture')}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  }),
    )
    add_fieldsets = (
        ('Creation Profile', {
            'classes': ('wide',),
            'fields': ('user', 'name', 'last_name', 'gender', 'age', 'profile_picture')
        }),
    )


@admin.register(UserAuth)
class UserAuthModelAdmin(admin.ModelAdmin):
    """Admin configuration for UserAuth model."""
    list_display = ['user_id', 'token_type', 'uuid', 'create_time', 'update_time', 'is_active', 'is_deleted']
    list_filter = ['user_id', 'token_type', 'is_active']
    search_fields = ['user_id', 'token_type', 'is_active']
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    ordering = ['-create_time']
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation User Auth',
         {'fields': ('user_id', 'token_type', 'uuid')}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
                  }),
    )
    add_fieldsets = (
        ('Creation User Auth', {
            'classes': ('wide',),
            'fields': ('user_id', 'token_type', 'uuid')
        }),
        ('Data', {'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
                  })
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role model."""
    list_display = ['code_discount', 'golden', 'silver', 'bronze',
                    'create_time', 'update_time', 'is_active', 'is_deleted']
    list_filter = ['code_discount', 'golden', 'silver', 'bronze', 'create_time', 'is_active']
    readonly_fields = ('create_time', 'update_time', 'is_active', 'is_deleted')
    ordering = ['-create_time']
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Role', {'fields': ('code_discount', 'golden', 'silver', 'bronze')}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
                  }),
    )
    add_fieldsets = (
        ('Creation Role', {
            'classes': ('wide',),
            'fields': ('code_discount', 'golden', 'silver', 'bronze')
        }),
        ('Data', {'fields': ('create_time', 'update_time', 'is_active', 'is_deleted')
                  })
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""

    list_display = ['user', 'name', 'last_name', 'gender', 'age', 'profile_picture', 'create_time', 'update_time',
                    'is_active',
                    'is_deleted']
    list_filter = ['user__username', 'name', 'age']
    search_fields = ['user__username', 'name', 'age', 'create_time', 'is_active']
    readonly_fields = ('is_deleted', 'create_time', 'update_time', 'is_active')
    ordering = ['-create_time']
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Profile',
         {'fields': (
             'user', 'name', 'last_name', 'gender', 'age', 'profile_picture'
         )}),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  }),
    )
    add_fieldsets = (
        ('Creation Profile', {
            'classes': ('wide',),
            'fields': ('user', 'name', 'last_name', 'gender', 'age', 'profile_picture')
        }),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  })
    )


@admin.register(CodeDiscount)
class CodeDiscountAdmin(admin.ModelAdmin):
    """Admin interface for managing CodeDiscount."""

    list_display = ['role_name', 'code', 'percentage_discount', 'numerical_discount', 'expiration_date', 'is_use',
                    'is_expired',
                    'is_active', 'is_deleted']
    list_filter = ['role_name', 'code', 'percentage_discount', 'numerical_discount', 'create_time', 'is_active']
    search_fields = ['role_name', 'code', 'percentage_discount',
                     'numerical_discount', 'create_time', 'is_active']
    readonly_fields = ('is_expired', 'create_time', 'update_time', 'is_active')
    ordering = ['-create_time']
    date_hierarchy = 'create_time'
    list_per_page = 30
    fieldsets = (
        ('Creation Address',
         {'fields': (
             'role_name', 'code', 'percentage_discount', 'numerical_discount', 'expiration_date', 'is_use',
         )}),
        ('Data', {'fields': ('is_expired', 'create_time', 'update_time', 'is_deleted', 'is_active')
                  }),
    )
    add_fieldsets = (
        ('Creation Address', {
            'classes': ('wide',),
            'fields': ('role', 'code', 'percentage_discount', 'is_active', 'is_deleted')
        }),
        ('Data', {'fields': ('create_time', 'update_time', 'is_deleted', 'is_active')
                  })
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin interface for managing addresses."""

    list_display = ['user', 'address_name', 'country', 'city',
                    'street', 'is_deleted', 'is_active']
    list_filter = ['user__username', 'address_name', 'city']
    search_fields = ['user__username', 'address_name', 'city']
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
         {'fields': ('email', 'phone_number', 'username', 'password')}),
        ('Permissions',
         {'fields': ('is_admin', 'is_superuser', 'is_staff', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'create_time', 'update_time', 'is_active', 'is_deleted',)}),
    )

    add_fieldsets = (
        ('Creation User', {
            'fields': ('email', 'phone_number', 'username', 'password1', 'password2')}
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

    inlines = (AddressInline, RoleInline, ProfileInline)

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
