from decouple import config # noqa
from time import timezone
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import redis
import pytz
from django.urls import reverse_lazy
from django.utils import timezone
from apps.core.otp_sms import CodeGenerator
from apps.account.form_data.forms import VerifyCodeForm
from apps.order.form_data import forms
from apps.core.mixin.mixin_views_template import HttpsOptionNotLogoutMixin as MustBeLogingCustomView


class PaymentOrderView(MustBeLogingCustomView):
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        self.code_generator = CodeGenerator()  # noqa
        self.form_class = forms.OrderPaymentForm  # noqa
        self.template_payment = 'order/payment/payment.html'  # noqa
        self.request_post = request.POST  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_payment, {'form': self.form_class()})

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request_post)
        if form.is_valid():
            order = forms.Order.objects.filter(order_item__user=request.user).latest('id')
            amount = order.finally_price
            expiration_date = form.cleaned_data['expiration_date']
            cardholder_name = form.cleaned_data['cardholder_name']
            card_number = form.cleaned_data['card_number']
            cvv = form.cleaned_data['cvv']

            order_payment_form_data = {
                'order': order.id,
                'amount': amount,
                'expiration_date': expiration_date.isoformat(),
                'cardholder_name': cardholder_name,
                'card_number': card_number,
                'cvv': cvv
            }
            request.session['order_payment_form_data'] = order_payment_form_data
            self.code_generator.generate_and_store_code(request.user.phone_number)
            return redirect('payment_verify_code')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)


class PaymentVerifyCodeView(MustBeLogingCustomView):
    http_method_names = ['get', 'post']

    def setup(self, request, *args, **kwargs):
        self.form_class = VerifyCodeForm  # noqa
        self.next_payment_order = reverse_lazy('payment_order')  # noqa
        self.next_page_payment_verify_code = reverse_lazy('payment_verify_code')  # noqa
        self.next_page_payment_success = reverse_lazy('payment_success')  # noqa
        self.template_payment_verify_code = 'order/payment/verify_code.html'  # noqa
        self.redis_client = redis.StrictRedis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=0)  # noqa
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_payment_verify_code, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_phone_number = request.user.phone_number
            code_instance = self.redis_client.get(user_phone_number)
            if not code_instance:  # noqa
                messages.error(request, _('Code is expired'), extra_tags='error')
            try:
                stored_code = code_instance.decode('utf-8')
            except AttributeError:
                return redirect(self.next_page_payment_verify_code)

            current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
            expiration_time = current_time + timezone.timedelta(minutes=2)
            if request.POST['code'] == stored_code and expiration_time > current_time:  # noqa
                with transaction.atomic():
                    order_payment_form_data = request.session.get('order_payment_form_data')
                    if order_payment_form_data:
                        with transaction.atomic():
                            order = forms.Order.objects.get(id=order_payment_form_data['order'])
                            create_payment = forms.OrderPayment.objects.create(
                                order=order,
                                amount=order_payment_form_data['amount'],
                                expiration_date=order_payment_form_data['expiration_date'],
                                cardholder_name=order_payment_form_data['cardholder_name'],
                                card_number=order_payment_form_data['card_number'],
                                cvv=order_payment_form_data['cvv'],
                                status='paid',
                                is_paid=True,
                                is_failed=False,
                                is_canceled=False
                            )
                        self.redis_client.delete(code_instance)
                        del request.session['order_payment_form_data']
                        return redirect(self.next_page_payment_success)

            elif expiration_time < current_time:
                self.redis_client.delete(code_instance)
                messages.error(request, _('Code is expired'), extra_tags='error')
                return redirect(self.next_payment_order)
        else:
            messages.error(request, _('Code is not valid'), extra_tags='error')
            return redirect(self.next_page_payment_verify_code)


class PaymentSuccessView(MustBeLogingCustomView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        try:
            order_payment = forms.OrderPayment.objects.filter(
                order__order_item__user=request.user,
                is_paid=True
            ).latest('id')
        except forms.OrderPayment.DoesNotExist:
            order_payment = None

        return render(request, 'order/payment/payment_success.html', {
            'order_payment': order_payment,
        })
