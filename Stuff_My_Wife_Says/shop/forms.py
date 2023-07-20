from django import forms
from .models import Order


SHIRT_SIZE_CHOICES = [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')]
QUANTITY_CHOICES = [(str(x), str(x)) for x in range(1, 11)] # list containing tuple integers as strings

class AddTShirtToCartForm(forms.Form):
    """T-shirt product details form for quantity and tshirt sizes"""
    size = forms.CharField(label='Size:', widget=forms.Select(choices=SHIRT_SIZE_CHOICES))
    quantity = forms.TypedChoiceField(label='Quantity:',
                                            coerce=int, # selected value is coerced into an integer
                                            choices=QUANTITY_CHOICES,
                                            widget=forms.Select(attrs={'class': 'form-control'}))


class AddMugToCartForm(forms.Form):
    """Mug product details form for quantity of mugs"""
    quantity = forms.TypedChoiceField(label='Quantity:',
                                      coerce=int,
                                      choices=QUANTITY_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-control'}))


class PaymentForm(forms.Form):
    """form for customer bank card details to make payment.
    NOTE: Nothing is done with the form data as this is just a personal project.
    If it went live than I would integrate a payment gateway such as PayPal API"""
    card_number = forms.CharField(label='Card Number', max_length=16)
    expiry = forms.CharField(label='Expiry Date', max_length=5)
    cvc = forms.CharField(label='CVC', max_length=4)
    name_on_card = forms.CharField(label='Name on card', max_length=100)


class CustomerDetailsForm(forms.Form):
    """form for collecting customer details for contact and delivery of their order"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'suburb', 'state', 'post_code']