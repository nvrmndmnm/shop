from django import forms
from cart.models import Order, Address


class OrderItemQuantityForm(forms.Form):
    quantity = forms.IntegerField(required=True, min_value=1)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'active']
