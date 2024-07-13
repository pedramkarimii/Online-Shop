from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from apps.account.form_data import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from apps.core.mixin.mixin_views_template import HttpsOptionNotLogoutMixin as MustBeLogingCustomView
from apps.order.models import Order, OrderItem
from apps.product.models import Product


class ProfileCreateView(MustBeLogingCustomView):
    """
    Handles the creation of user profiles.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form, next page1, page2, template name.
        """
        self.form_class = forms.ProfileCreateForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_create_profile = reverse_lazy('create_profile')  # noqa
        self.template_create_profile = 'user/profile/create_profile.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        Renders the form for creating a user profile.
        """
        form = self.form_class(instance=request.user)
        return render(request, self.template_create_profile, {'form': form})

    def post(self, request):
        """
        Handles form submission for creating a user profile.
        """
        try:
            profile = request.user.profile
        except forms.Profile.DoesNotExist:
            profile = None

        form = self.form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()
            messages.success(
                request,
                _('Your profile has been created successfully'),
                extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(
                request,
                _('Your profile has not been created successfully'), extra_tags='error')
            return redirect(self.next_page_create_profile)


class ProfileUpdateView(MustBeLogingCustomView):
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form, next page1, page2, template name.
        """
        self.profile_instance = get_object_or_404(forms.Profile, pk=kwargs['pk'])  # noqa
        self.form_class = forms.ProfileUpdateForm  # noqa
        self.template_chnage_info_profile = 'user/profile/change_info_profile.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Renders the form for updating the user's profile.
        """
        form = self.form_class(instance=self.profile_instance)
        return render(request, self.template_chnage_info_profile, {'form': form, 'profile': self.profile_instance})

    def post(self, request, *args, **kwargs):
        """
        Handles form submission for updating the user's profile.
        """
        form = self.form_class(self.request_post, self.request_files, instance=self.profile_instance)  # noqa
        if form.is_valid():  # noqa
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, _(f'Profile updated successfully {profile.name}.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating Profile.'), extra_tags='error')


class ProfileDetailView(MustBeLogingCustomView, DetailView):
    http_method_names = ['get']
    model = forms.Profile  # Set the model

    def setup(self, request, *args, **kwargs):
        """
        Initialize the context object name and template name.
        """
        self.context_object_name = 'profile'
        self.template_name = 'user/profile/profile.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Returns the profile instance for the current user.
        """
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """
        Adds additional context data for rendering the template.
        """
        context = super().get_context_data(**kwargs)
        profile = self.object

        addresses = forms.Address.objects.filter(user=self.request.user)
        user_cods_discount = forms.Role.objects.filter(
            Q(golden=self.request.user) |
            Q(silver=self.request.user) |
            Q(bronze=self.request.user) |
            Q(seller=self.request.user)
        ).values_list('code_discount', flat=True)
        code_discounts = forms.CodeDiscount.objects.filter(id__in=user_cods_discount)
        orders = Order.objects.filter(order_item__user=self.request.user).distinct()
        products = Product.objects.all()
        order_items = OrderItem.objects.filter(order_items__order_item__product__in=
                                               products.all())
        unique_product_names = set()
        for order_item in order_items:
            if order_item.user == self.request.user:
                unique_product_names.add(order_item.product.name)
        name_product_in_order = ','.join(unique_product_names)
        context['name_product_in_order'] = name_product_in_order
        context['cods_discount'] = code_discounts
        context['profile'] = profile
        context['orders'] = orders

        context['addresses'] = addresses

        return context


class ProfileDeleteView(DetailView, MustBeLogingCustomView):
    """
    View for displaying profile details and providing an option for soft deletion.
    """
    model = forms.Profile
    template_name = 'user/profile/profile_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display profile details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'profile': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the profile.
        """
        profile = self.get_object()
        forms.Profile.soft_delete.filter(pk=profile.id).delete()
        messages.success(request, _(f'Profile has been successfully soft deleted {profile.name}.'),
                         extra_tags='success')
        return redirect('home')
