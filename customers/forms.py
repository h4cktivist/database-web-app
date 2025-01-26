from django import forms

from .models import Customers


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'pattern': '\+7\d{10}'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон (в формате +7XXXXXXXXXX)',
            'email': 'Email',
        }
