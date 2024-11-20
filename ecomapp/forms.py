from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address1', 'address2', 'city', 'state', 'zip_code']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone
