from django.urls import path
from django.views.generic import TemplateView

from apps.order.views.views_template import views_payment

urlpatterns = [

    path('payment-order/', views_payment.PaymentOrderView.as_view(),
         name='payment_order'),
    path('payment-success/', views_payment.PaymentSuccessView.as_view(),
         name='payment_success'),
    path('payment-failed/', TemplateView.as_view(template_name='order/payment/payment_failed.html'),
         name='payment_failed'),
    path('payment-canceled/', TemplateView.as_view(template_name='order/payment/payment_canceled.html'),
         name='payment_canceled'),
    path('payment-verify-code/',  views_payment.PaymentVerifyCodeView.as_view(),
         name='payment_verify_code'),
]
