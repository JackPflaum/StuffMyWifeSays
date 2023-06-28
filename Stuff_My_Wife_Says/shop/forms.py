from django import forms


SHIRT_SIZE_CHOICES = [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')]
QUANTITY_CHOICES = [(str(x), str(x)) for x in range(1, 11)] # list containing tuple integers as strings

class AddProductToCartForm(forms.Form):
    """Product details form for purchase quantity and tshirt sizes"""
    size = forms.CharField(label='Size:', widget=forms.Select(choices=SHIRT_SIZE_CHOICES))
    quantity = forms.TypedChoiceField(label='Quantity:',
                                            coerce=int, # selected value is coerced into an integer
                                            choices=QUANTITY_CHOICES,
                                            widget=forms.Select(attrs={'class': 'form-control'}))