from django.views import generic
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from apps.product.form_data import forms
from apps.core.permission.template_permission_admin import CRUD


class DiscountCreateView(CRUD.AdminPermissionRequiredMixinView):
    """
    Create a new discount.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.form_class = forms.DiscountCreateForm  # noqa
        self.next_page_discount_create = reverse_lazy('discount_create')  # noqa
        self.template_discount_create = 'product/discount/discount_create.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        function to handle get request on the view. Renders the form for creating a new discount.
        """
        return render(request, self.template_discount_create, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        """
        function to handle post request on the view. Creates a new discount based on the form data.
        Validates the form data and saves the discount if the form is valid. If the form is invalid,
        it renders the form with error messages.
        :param request: The HTTP request object
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: The rendered template response
        """
        form = self.form_class(self.request_post)  # noqa

        if form.is_valid():
            percentage_discount = form.cleaned_data.get('percentage_discount')
            numerical_discount = form.cleaned_data.get('numerical_discount')

            if not percentage_discount and not numerical_discount:
                messages.error(request, _('Either percentage discount or numerical discount must be provided.'),
                               extra_tags='error')

            if percentage_discount and numerical_discount:
                messages.error(request, _('Only one type of discount can be provided.'), extra_tags='error')
                return redirect(self.next_page_discount_create)
            discount = form.save(commit=False)
            discount.save()
            messages.success(request, _(f'Discount created successfully Date:{discount.expiration_date} .'),
                             extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error creating discount.'), extra_tags='error')
        return render(request, self.template_discount_create, {'form': form})


class AdminDiscountListView(CRUD.AdminPermissionRequiredMixinView, generic.ListView):
    """
    List all discounts for admin or supervisor.
    """
    http_method_names = ['get']  # noqa
    model = forms.Discount

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'discounts'
        self.template_name = 'user/detail/admin/admin_discount.html'
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        """
        function to get the queryset for the view.
        """
        return forms.Discount.objects.all()

    def get_context_data(self, **kwargs):
        """
        function to get the context data for the view.
        """
        context = super().get_context_data(**kwargs)  # noqa
        discounts = forms.Discount.objects.all()
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['admin_discounts'] = discounts
            return context
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name='Supervisor').exists():
            context['supervisor_discounts'] = discounts
            return context


class DiscountDetailView(CRUD.AdminPermissionRequiredMixinView, DetailView):
    """
    Detail view for a discount.
    """
    http_method_names = ['get']  # noqa
    model = forms.Discount

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.context_object_name = 'address'
        self.template_name = 'product/discount/discount.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        function to get the object for the view.
        """
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
        """
        function to get the context data for the view.
        :param kwargs: Keyword arguments
        :return: The context data for the view
        """
        context = super().get_context_data(**kwargs)
        discounts = forms.Discount.objects.all()
        context['discounts'] = discounts
        return context


class DiscountUpdateView(CRUD.AdminPermissionRequiredMixinView):
    """
    Update an existing discount.
    """

    def setup(self, request, *args, **kwargs):
        """
        function to set up the view before rendering.
        """
        self.form_class = forms.DiscountUpdateForm  # noqa
        self.template_discount_update = 'product/discount/discount_update.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        function to handle get request on the view. Renders the form for updating an existing discount.
        """
        form = self.form_class(instance=self.discount_instance)
        return render(request, self.template_discount_update, {'form': form, 'discount': self.discount_instance})

    def post(self, request, *args, **kwargs):
        """
        function to handle post request on the view. Updates an existing discount based on the form data.
        Validates the form data and saves the discount if the form is valid. If the form is invalid,
        it renders the form with error messages.
        :param request: The HTTP request object
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: The rendered template response
        """
        form = self.form_class(self.request_post, instance=self.discount_instance)  # noqa
        if form.is_valid():  # noqa
            discount = form.save(commit=False)
            discount.save()
            messages.success(request, _(f'Discount updated successfully Date:{discount.expiration_date} .'),
                             extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating discount.'), extra_tags='error')


class DiscountDeleteView(CRUD.AdminPermissionRequiredMixinView, DetailView):
    """
    View for displaying discount details and providing an option for soft deletion.
    """
    model = forms.Discount
    template_name = 'product/discount/discount_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display discount details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'discount': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the discount.
        """
        discount = self.get_object()
        forms.Discount.objects.filter(pk=discount.id).delete()
        messages.success(request, _(f'Discount has been successfully soft deleted.'), extra_tags='success')
        return redirect('home')
