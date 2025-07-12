from django import forms
from products.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'date_from', 'date_to']
        labels = {
            'name': 'Імʼя',
            'phone': 'Телефон',
            'email': 'Email',
            'date_from': 'Дата з',
            'date_to': 'Дата по',
        }
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'}),
        }
