from apps.account.models import CodeDiscount, Role
from apps.core.mixin.mixin_views_template import HttpsOptionNotLogoutMixin, messages, PermissionRequiredMixin, \
    redirect, get_object_or_404
from apps.product.models import Product, Brand, Category, AddToInventory, Discount, Inventory


class MainPermissionRequiredMixinView(PermissionRequiredMixin, HttpsOptionNotLogoutMixin):
    """
    Defines a view mixin class that combines permission checking and HTTPS options for user sessions.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Overrides the dispatch method to check permissions and fetch instances of various
        models based on the URL parameter `pk`. If an instance is found, it assigns it to an
        instance variable. If permission is denied, it redirects the user and displays an error message.
        """

        try:  # noqa
            self.discount_code_instance = get_object_or_404(CodeDiscount, pk=kwargs['pk'])  # noqa

        except Exception:  # noqa
            pass
        try:  # noqa
            self.role_instance = get_object_or_404(Role, pk=kwargs['pk'])  # noqa

        except Exception:  # noqa
            pass
        try:
            self.inventory_instance = get_object_or_404(Inventory, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass
        try:
            self.add_to_inventory_instance = get_object_or_404(AddToInventory, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass
        try:  # noqa
            self.discount_instance = get_object_or_404(Discount, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass
        try:  # noqa
            self.category_instance = get_object_or_404(Category, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass
        try:
            self.brand_instance = get_object_or_404(Brand, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass
        try:
            self.product_instance = get_object_or_404(Product, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass

        if not self.has_permission():
            messages.error(request, 'You do not have permission.', extra_tags='error')
            return redirect(self.next_page_home)
        return super().dispatch(request, *args, **kwargs)

    def get_permission_required(self):
        """
        Returns the required permission for the view, which is set by subclasses.
        """

        return self.permission_required


class SellerOrAdminCreatePermissionRequiredMixinView(MainPermissionRequiredMixinView):
    """
    Defines a permission class for creating operations, checking if the user is authenticated and
    either a superuser, staff, or belongs to the 'Seller' group.
    """

    http_method_names = ['get', 'post']

    def has_permission(self):
        """
        Checks if the user is authenticated and either a superuser, staff, or belongs to the 'Seller' group.
        Returns True if the user has permission, False otherwise.
        """

        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
                or self.request.user.groups.filter(name='Seller').exists()
        ):
            return True

        return False


class SellerOrAdminOrSupervisorDetailPermissionRequiredMixinView(MainPermissionRequiredMixinView):
    """
    Defines a permission class for viewing details, checking if the user is authenticated and either
    a superuser, staff, or belongs to either the 'Seller' or 'Supervisor' group.
    """

    http_method_names = ['get']
    permission_required = (
        'Supervisor',
    )

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
                or self.request.user.groups.filter(name='Seller').exists()
                or self.request.user.groups.filter(name='Supervisor').exists()
        ):
            return True

        return False


class SellerOrAdminBrandUpdateOrDeletePermissionRequiredMixinView(MainPermissionRequiredMixinView):  # noqa
    """
    Defines a permission class for updating or deleting brands, checking if the user is authenticated
    and either a superuser, staff, or if the user is the owner of the brand being accessed.
    """

    http_method_names = ['get', 'post']  # noqa

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
                or (self.request.user.groups.filter(name='Seller').exists()
                    and self.brand_instance.user == self.request.user)

        ):
            return True
        else:
            return False

        # return False


class SellerOrAdminProductUpdateOrDeletePermissionRequiredMixinView(MainPermissionRequiredMixinView):  # noqa
    """
    Defines a permission class for updating or deleting products, checking if the user is authenticated
    and either a superuser, staff, or if the user is the owner of the brand associated with the product being accessed.
    """

    http_method_names = ['get', 'post']  # noqa

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
                or (self.request.user.groups.filter(name='Seller').exists()
                    and self.product_instance.brand.user == self.request.user)

        ):
            return True

        return False
