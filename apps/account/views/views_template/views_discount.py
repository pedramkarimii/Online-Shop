from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import generic
from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.core.permission.template_permission_admin import CRUD


class DiscountCodCreateView(CRUD.AdminPermissionRequiredMixinView):
    def setup(self, request, *args, **kwargs):
        """Initialize the success_url."""
        self.form_class = forms.DiscountCodeCreateForm  # noqa
        self.next_page_discount_create = reverse_lazy('discount_cod_create')  # noqa
        self.template_discount_create = 'user/discount_cod/discount_cod_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_discount_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post)
        if form.is_valid():
            discount_cod = form.save(commit=False)
            discount_cod.save()
            messages.success(request, _(f'Discount created successfully {discount_cod.role_name}.'),
                             extra_tags='success')
        else:
            messages.error(request, _('No eligible users found for the discount.'), extra_tags='error')
        return redirect(self.next_page_home)


class DiscountCodUpdateView(CRUD.AdminPermissionRequiredMixinView):
    def setup(self, request, *args, **kwargs):

        self.form_class = forms.DiscountCodeUpdateForm  # noqa
        self.template_discount_cod_update = 'user/discount_cod/discount_cod_update.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.discount_code_instance)
        return render(request, self.template_discount_cod_update,
                      {'form': form, 'discount_cod': self.discount_code_instance})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post, instance=self.discount_code_instance)  # noqa
        if form.is_valid():  # noqa
            discount_cod = form.save(commit=False)
            discount_cod.save()
            messages.success(request, _(f'Discount Code updated successfully {discount_cod.role_name}.'),
                             extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating Discount Code .'), extra_tags='error')


class AdminDiscountCodDetailView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    http_method_names = ['get']  # noqa
    model = forms.CodeDiscount

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'discount_cod'
        self.template_name = 'user/detail/admin/admin_discount_cod.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return forms.CodeDiscount.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        discount_cods = forms.CodeDiscount.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_discount_cod'] = discount_cods
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_discount_cod'] = discount_cods
            return context


class DiscountCodDetailView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    http_method_names = ['get']  # noqa
    model = forms.CodeDiscount

    def setup(self, request, *args, **kwargs):
        self.context_object_name = 'discount_cod'
        self.template_name = 'user/discount_cod/discount_cod.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Return the discounts cod instance based on the URL kwargs."""  # noqa
        queryset = self.get_queryset()  # noqa
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return render(self.request, 'http_method/http_404.html')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discount_cods = forms.CodeDiscount.objects.all()
        context['discount_cods'] = discount_cods
        return context


class DiscountCodDeleteView(CRUD.AdminPermissionRequiredMixinView, generic.DetailView):
    """
    View for displaying code discount details and providing an option for soft deletion.
    """
    model = forms.CodeDiscount
    template_name = 'user/discount_cod/discount_cod_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display code discount details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'code_discount': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the code discount.
        """
        code_discount = self.get_object()
        forms.CodeDiscount.soft_delete.filter(pk=code_discount.id).delete()
        messages.success(request, _(f'Code Discount has been successfully soft deleted.'), extra_tags='success')
        return redirect(self.next_page_home)
