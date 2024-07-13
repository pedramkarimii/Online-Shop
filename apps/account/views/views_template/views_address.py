from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.account.form_data import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from apps.core.mixin.mixin_views_template import HttpsOptionNotLogoutMixin as MustBeLogingCustomView


class AddressCreateView(MustBeLogingCustomView):
    """
    Handles the creation of user addresses.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """
        Initialize the form, next page1, page2, template name.
        """
        self.form_class = forms.CreateAddressForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.next_page_create_address = reverse_lazy('create_address')  # noqa
        self.template_create_address = 'user/address/create_address.html'  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        """
        Renders the form for creating a user address.
        """
        addresses = request.user.address_set.all()  # Retrieve the user's addresses
        form = self.form_class(initial={'addresses': addresses})  # Pass the addresses to the form
        return render(request, self.template_create_address, {'form': form})

    def post(self, request):
        """
        Handles form submission for creating a user address.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, _(f'Your address has been created successfully {address.address_name}.'),
                             extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(
                request,
                _('Your address has not been created successfully'),
                extra_tags='error')
            return redirect(self.next_page_create_address)


class AddressDetailView(MustBeLogingCustomView, DetailView):
    """
    View to display the details of a user's address.
    """
    http_method_names = ['get']  # noqa
    model = forms.Address

    def setup(self, request, *args, **kwargs):
        """
        Initialize the context object name and template name.
        """
        self.context_object_name = 'address'
        self.template_name = 'user/address/address.html'
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """ Return the Address instance based on the URL kwargs."""  # noqa
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
        addresses = forms.Address.objects.filter(user=self.request.user)
        context['addresses'] = addresses
        return context


class AddressUpdateView(MustBeLogingCustomView):
    """
    View for updating user addresses.
    """
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        """

        """
        self.address_instance = get_object_or_404(forms.Address, pk=kwargs['pk'])  # noqa
        self.form_class = forms.UpdateAddressForm  # noqa
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_address_update = 'user/address/change_info_address.html'  # noqa
        self.request_files = request.FILES  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Renders the form for updating the user's address.
        """
        form = self.form_class(instance=self.address_instance)
        return render(request, self.template_address_update, {'form': form, 'address': self.address_instance})

    def post(self, request, *args, **kwargs):
        """
        Handles form submission for updating the user's address.
        """
        form = self.form_class(self.request_post, self.request_files, instance=self.address_instance)  # noqa
        if form.is_valid():  # noqa
            address = form.save(commit=False)
            address.save()
            messages.success(request, _(f'Address updated successfully {address.address_name}.'), extra_tags='success')
            return redirect(self.next_page_home)
        else:
            messages.error(request, _(f'Error updating Address.'), extra_tags='error')


class AddressDeleteView(DetailView, MustBeLogingCustomView):
    """
    View for displaying address details and providing an option for soft deletion.
    """
    model = forms.Address
    template_name = 'user/address/address_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Display address details.
        """
        self.object = self.get_object()  # noqa
        return render(request, self.template_name, {'address': self.object})

    def post(self, request, *args, **kwargs):
        """
        Handle soft deletion of the address.
        """
        address = self.get_object()
        forms.Address.soft_delete.filter(pk=address.id).delete()
        messages.success(request, -(f'Address has been successfully soft deleted {address.name}.'),  # noqa
                         extra_tags='success')
        return redirect('home')
