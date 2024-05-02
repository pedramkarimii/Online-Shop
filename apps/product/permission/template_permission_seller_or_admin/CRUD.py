from apps.account.models import CodeDiscount, Role
from apps.core.mixin.mixin_views_template import HttpsOptionNotLogoutMixin, messages, PermissionRequiredMixin, \
    redirect, get_object_or_404
from apps.product.models import Product, Brand, Category, WarehouseKeeper, Discount


class MainPermissionRequiredMixinView(PermissionRequiredMixin, HttpsOptionNotLogoutMixin):
    permission_required = (
        'Seller',
    )

    def dispatch(self, request, *args, **kwargs):
        try:  # noqa
            self.discount_code_instance = get_object_or_404(CodeDiscount, pk=kwargs['pk'])  # noqa

        except Exception:  # noqa
            pass
        try:  # noqa
            self.role_instance = get_object_or_404(Role, pk=kwargs['pk'])  # noqa

        except Exception:  # noqa
            pass
        try:
            self.warehouse_keeper_instance = get_object_or_404(WarehouseKeeper, pk=kwargs['pk'])  # noqa
        except Exception:  # noqa
            pass
        try: # noqa
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
        Returns the list of permissions required to access the view.
        """
        return self.permission_required


class SellerOrAdminCreatePermissionRequiredMixinView(MainPermissionRequiredMixinView):
    http_method_names = ['get', 'post']

    def has_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_active and (
                self.request.user.is_superuser
                or self.request.user.is_staff
                or self.request.user.groups.filter(name='Seller').exists()

        ):
            return True

        return False


class SellerOrAdminOrSupervisorDetailPermissionRequiredMixinView(MainPermissionRequiredMixinView):
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
