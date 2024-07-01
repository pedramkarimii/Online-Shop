from django.urls import path
from django.views.generic import TemplateView
from apps.order.views.views_template import views_payment

"""
This code defines several URL patterns for handling payment-related operations using class-based views and 
template views.
- The `urlpatterns` list contains five URL patterns.
- Each `path` function call defines a unique URL route and associates it with a specific view.
  - `'payment-order/'`: Maps to `views_payment.PaymentOrderView.as_view()`, allowing users to initiate a payment order.
  - `'payment-success/'`: Maps to `views_payment.PaymentSuccessView.as_view()`, displaying a success message after
   a successful payment.
  - `'payment-failed/'`: Maps to `TemplateView` with the template name `'order/payment/payment_failed.html'`,
   displaying a page indicating a failed payment.
  - `'payment-canceled/'`: Maps to `TemplateView` with the template name `'order/payment/payment_canceled.html'`,
   displaying a page indicating a canceled payment.
  - `'payment-verify-code/'`: Maps to `views_payment.PaymentVerifyCodeView.as_view()`, handling verification 
  of payment codes.
- Each URL pattern is assigned a unique `name`, which can be used to reference the URL pattern in templates or 
other parts of the Django application.
These patterns provide endpoints for handling various stages and outcomes of the payment process within the
 web application.
"""
urlpatterns = [

    path('payment-order/', views_payment.PaymentOrderView.as_view(),
         name='payment_order'),
    path('payment-success/', views_payment.PaymentSuccessView.as_view(),
         name='payment_success'),
    path('payment-failed/', TemplateView.as_view(template_name='order/payment/payment_failed.html'),
         name='payment_failed'),
    path('payment-canceled/', TemplateView.as_view(template_name='order/payment/payment_canceled.html'),
         name='payment_canceled'),
    path('payment-verify-code/', views_payment.PaymentVerifyCodeView.as_view(),
         name='payment_verify_code'),
]
