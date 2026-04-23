from django import forms
from cart.models import Order


class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('online', 'Pay online'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['address', 'phone', 'payment_method']