from apps.product.permission.template_permission_seller_or_admin.CRUD import MainPermissionRequiredMixinView


class AdminPermissionRequiredMixinView(MainPermissionRequiredMixinView):
    """Mixin class for views requiring admin permissions.

        Inherits from MainPermissionRequiredMixinView and extends it with additional
        permission checks specific to admin users. Overrides the has_permission method
        to check if the request user is authenticated, active, and either a superuser
        or staff member.

        Attributes:
            http_method_names (list): Allowed HTTP methods for the view.

        Methods:
            has_permission(self):
                Checks if the request user meets the criteria for admin permissions.

        """
    http_method_names = ['get', 'post']

    def has_permission(self):
        """Check if the request user has admin permissions."""
        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
        ):
            return True

        return False
