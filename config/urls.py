from django.conf import settings
from django.contrib import admin
from django.urls import path, include

"""Define URL patterns for the entire application."""
urlpatterns = [
    path("", include("apps.public.urls")),
    path("", include("apps.account.urls")),
    path("", include("apps.order.urls")),
    path("", include("apps.product.urls")),
    path("", include("utility.bucket.urls")),
]

"""Check if the application is in debug mode."""
if settings.DEBUG:
    from django.conf.urls.static import static

    """Add URL pattern for accessing the Django admin site."""
    urlpatterns += (
            [path("admin/", admin.site.urls)]
            + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
            + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    """Customize Django admin interface titles."""
    admin.site.site_header = 'Online Shop'
    admin.site.site_title = 'Online Shop Administration'
    admin.site.index_title = 'Welcome To Online Shop Administration'
