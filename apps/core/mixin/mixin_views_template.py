from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View


class HttpsOptionNotLogoutMixin(View):
    def setup(self, request, *args, **kwargs):  # noqa
        """Initialize the next_page_create_profile, get profile, authenticate."""
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_http_method_not_allowed = 'http_method/http_404.html'  # noqa
        self.authenticate_user = request.user.is_authenticated  # noqa
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch method to handle user authentication status.
        Redirects non-authenticated users to the home page with an error message.
        """
        if not self.authenticate_user:
            messages.error(
                request,
                'You are not login please first login your account.',
                extra_tags='error',
            )
            return redirect(self.next_page_home)

        return super().dispatch(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """
        Handles OPTIONS requests.
        Returns a response with the allowed HTTP methods.
        """
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'
        return response

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        Handles HTTP method not allowed requests.
        Returns a response with the allowed HTTP methods.
        This method is called when a request is made with an unsupported HTTP method.
        """
        super().http_method_not_allowed(request, *args, **kwargs)
        return render(request, self.template_http_method_not_allowed)


class HttpsOptionLoginMixin(View):
    def setup(self, request, *args, **kwargs):  # noqa
        """Initialize the next_page_create_profile, get profile, authenticate."""
        self.next_page_home = reverse_lazy('home')  # noqa
        self.template_http_method_not_allowed = 'http_method/http_404.html'  # noqa
        self.authenticate_user = request.user.is_authenticated  # noqa
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch method to handle user authentication status.
        If the user is authenticated, redirect to the home page.
        Otherwise, proceed with the default dispatch behavior.
        """
        if self.authenticate_user:
            messages.warning(request, 'You are already login.', extra_tags='warning')
            return redirect(self.next_page_home)

        else:
            return super().dispatch(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """
        Handles OPTIONS requests.
        Returns a response with the allowed HTTP methods.
        """
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'
        return response

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        Handles HTTP method not allowed requests.
        Returns a response with the allowed HTTP methods.
        This method is called when a request is made with an unsupported HTTP method.
        """
        super().http_method_not_allowed(request, *args, **kwargs)
        return render(request, self.template_http_method_not_allowed)
