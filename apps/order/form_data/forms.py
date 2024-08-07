import datetime
from django import forms
from apps.core import validators
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from apps.order.models import OrderItem, Order, OrderPayment


class OrderItemForm(forms.ModelForm):
    """
    Form for creating and updating OrderItem objects.
    """

    class Meta:
        model = OrderItem
        fields = [
            'user', 'product', 'quantity'
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }
        labels = {
            'user': _('User'),
            'product': _('Product'),
            'quantity': _('Quantity')
        }
        help_texts = {
            'user': _('Select the user who placed the order.'),
            'product': _('Select the product being ordered.'),
            'quantity': _('Enter the quantity of the product.')
        }
        error_messages = {
            'user': {
                'required': _('User is required.')
            },
            'product': {
                'required': _('Product is required.')
            },
            'quantity': {
                'required': _('Quantity is required.'),
                'invalid': _('Quantity must be a positive integer.')
            }
        }
        validators = {
            'quantity': [validators.QuantityValidators()]
        }

    def clean_quantity(self):
        """
        Custom validator for quantity field to ensure it is positive.
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError(_('Quantity must be a positive integer.'))
        return quantity

    def save(self, commit=True):
        """
        Method to save the OrderItem object.
        """
        order_item = super().save(commit=False)
        order_item.user = self.cleaned_data['user']
        order_item.product = self.cleaned_data['product']
        order_item.quantity = self.cleaned_data['quantity']
        order_item.total_price = order_item.product.price * order_item.quantity
        if commit:
            order_item.save()
        return order_item


class OrderForm(forms.ModelForm):
    """
    Form for creating and updating Order objects.
    """

    class Meta:
        model = Order
        fields = ['address', 'payment_method', 'code_discount', 'finally_price']

        widgets = {
            'user': forms.HiddenInput(),
            'order_item': forms.HiddenInput(),
            'address': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'status': forms.HiddenInput(),
            'transaction_id': forms.HiddenInput(),
            'payment_method': forms.Select(
                attrs={'class': 'form-select mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'code_discount': forms.TextInput(
                attrs={'class': 'form-control mt-1 pt-2 py-2 px-4 focus:ring-indigo-500 focus:border-indigo-500 '
                                'block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'finally_price': forms.HiddenInput(),
            'time_accepted_order': forms.HiddenInput(),
            'accepted_order': forms.HiddenInput(),
            'time_shipped_order': forms.HiddenInput(),
            'shipped_order': forms.HiddenInput(),
            'time_deliver_order': forms.HiddenInput(),
            'deliver_order': forms.HiddenInput(),
            'time_rejected_order': forms.HiddenInput(),
            'rejected_order': forms.HiddenInput(),
            'time_cancelled_order': forms.HiddenInput(),
            'cancelled_order': forms.HiddenInput(),
        }
        labels = {
            'user': _('User'),
            'order_item': _('Order Item'),
            'address': _('Address'),
            'status': _('Status'),
            'transaction_id': _('Transaction ID'),
            'payment_method': _('Payment Method'),
            'code_discount': _('Code Discount'),
            'finally_price': _('Finally Price'),
            'time_accepted_order': _('Time Accepted Order'),
            'accepted_order': _('Accepted Order'),
            'time_shipped_order': _('Time Shipped Order'),
            'shipped_order': _('Shipped Order'),
            'time_deliver_order': _('Time Deliver Order'),
            'deliver_order': _('Deliver Order'),
            'time_rejected_order': _('Time Rejected Order'),
            'rejected_order': _('Rejected Order'),
            'time_cancelled_order': _('Time Cancelled Order'),
            'cancelled_order': _('Cancelled Order'),
        }
        help_texts = {
            'user': _('Select the user who placed the order.'),
            'order_item': _('Select the order item.'),
            'address': _('Select the address.'),
            'status': _('Select the status.'),
            'transaction_id': _('Enter the transaction ID.'),
            'payment_method': _('Select the payment method.'),
            'code_discount': _('Enter the code discount.'),
            'finally_price': _('Enter the finally price.'),
            'time_accepted_order': _('Enter the time accepted order.'),
            'accepted_order': _('Check the accepted order.'),
            'time_shipped_order': _('Enter the time shipped order.'),
            'shipped_order': _('Check the shipped order.'),
            'time_deliver_order': _('Enter the time deliver order.'),
            'deliver_order': _('Check the deliver order.'),
            'time_rejected_order': _('Enter the time rejected order.'),
            'rejected_order': _('Check the rejected order.'),
            'time_cancelled_order': _('Enter the time cancelled order.'),
            'cancelled_order': _('Check the cancelled order.'),
        }
        error_messages = {
            'user': {
                'required': _('User is required.')
            },
            'order_item': {
                'required': _('Order item is required.')
            },
            'address': {
                'required': _('Address is required.')
            },
            'status': {
                'required': _('Status is required.')
            },
            'transaction_id': {
                'required': _('Transaction ID is required.')
            },
            'payment_method': {
                'required': _('Payment method is required.')
            },
            'code_discount': {
                'required': _('Code discount is required.')
            },
            'finally_price': {
                'required': _('Finally price is required.'),
                'invalid': _('Finally price must be a positive integer.')
            },
            'time_accepted_order': {
                'required': _('Time accepted order is required.')
            },
            'accepted_order': {
                'required': _('Accepted order is required.')
            },
            'time_shipped_order': {
                'required': _('Time shipped order is required.')
            },
            'shipped_order': {
                'required': _('Shipped order is required.')
            },
            'time_deliver_order': {
                'required': _('Time deliver order is required.')
            },
            'deliver_order': {
                'required': _('Deliver order is required.')
            },
            'time_rejected_order': {
                'required': _('Time rejected order is required.')
            },
            'rejected_order': {
                'required': _('Rejected order is required.')
            },
            'time_cancelled_order': {
                'required': _('Time cancelled order is required.')
            },
            'cancelled_order': {
                'required': _('Cancelled order is required.')
            },
        }
        validators = {
            'finally_price': [validators.FinallyPriceValidator],
        }

    def clean_total_price(self):
        """
        Custom validator for total_price field to ensure it is positive.
        """
        total_price = self.cleaned_data.get('finally_price')
        if total_price < 1:
            raise ValidationError(_('Finally price must be a positive integer.'))
        return total_price

    def save(self, commit=True):
        """
        Method to save the Order object.
        """
        order = super().save(commit=False)
        order.address = self.cleaned_data['address']
        order.payment_method = self.cleaned_data['payment_method']
        order.code_discount = self.cleaned_data['code_discount']
        order.finally_price = self.cleaned_data['finally_price']
        if commit:
            order.save()
        return order


class OrderPaymentForm(forms.ModelForm):
    """
    Form for creating and updating OrderPayment objects.
    """

    class Meta:
        model = OrderPayment
        fields = [
            'cardholder_name', 'card_number', 'expiration_date', 'cvv'
        ]
        widgets = {
            'cardholder_name': forms.TextInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 bg-with mb-8 focus:ring-indigo-500'
                             ' focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'card_number': forms.TextInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 bg-with mb-8 focus:ring-indigo-500'
                             ' focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'expiration_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': _('YYYY-MM-DD'), 'type': 'date'}),
            'cvv': forms.TextInput(
                attrs={
                    'class': 'form-control mt-1 pt-2 py-2 px-4 bg-with mb-8 focus:ring-indigo-500'
                             ' focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
        }
        labels = {
            'order': _('Order'),
            'amount': _('Amount'),
            'cardholder_name': _('Cardholder Name'),
            'card_number': _('Card Number'),
            'expiration_date': _('Expiration Date'),
            'cvv': _('CVV'),
        }
        help_texts = {
            'order': _('Select the order.'),
            'amount': _('Enter the amount.'),
            'cardholder_name': _('Enter the cardholder name.'),
            'card_number': _('Enter the card number.'),
            'expiration_date': _('Select the expiration date.'),
            'cvv': _('Enter the CVV.'),
        }
        error_messages = {
            'order': {
                'required': _('Order is required.')
            },
            'amount': {
                'required': _('Amount is required.')
            },
            'cardholder_name': {
                'required': _('Cardholder name is required.')
            },
            'card_number': {
                'required': _('Card number is required.')
            },
            'expiration_date': {
                'required': _('Expiration date is required.')
            },
            'cvv': {
                'required': _('CVV is required.')
            },
        }
        validators = {
            'cardholder_name': [validators.CardholderNameValidator],
            'amount': [validators.AmountValidator],
            'card_number': [validators.CardNumberValidator],
            'cvv': [validators.CVVValidator],
        }

    def clean_expiration_date(self):
        """
        Custom validator for expiration_date field to ensure it is in the future.
        """
        expiration_date = self.cleaned_data.get('expiration_date')

        if not isinstance(expiration_date, datetime.date):
            raise ValidationError(_('Invalid date format.'))

        if expiration_date < datetime.date.today():
            raise ValidationError(_('Expiration date must be in the future.'))
        return expiration_date

    def save(self, commit=True):
        """
        Method to save the OrderPayment object.
        """
        order_payment = super().save(commit=False)
        print(self.cleaned_data['cardholder_name'])
        order_payment.cardholder_name = self.cleaned_data['cardholder_name']
        order_payment.card_number = self.cleaned_data['card_number']
        order_payment.expiration_date = self.cleaned_data['expiration_date']
        order_payment.cvv = self.cleaned_data['cvv']
        if commit:
            order_payment.save()
        return order_payment
