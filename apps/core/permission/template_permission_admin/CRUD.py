from apps.product.permission.template_permission_seller_or_admin.CRUD import MainPermissionRequiredMixinView


class AdminPermissionRequiredMixinView(MainPermissionRequiredMixinView):
    http_method_names = ['get', 'post']

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
        ):
            return True

        return False
