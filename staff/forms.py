from django import forms

from .models import Positions, Staff


class PositionsForm(forms.ModelForm):
    class Meta:
        model = Positions
        fields = ['title']
        labels = {
            'title': 'Название должности',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'middle_name', 'position', 'phone']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'position': 'Должность',
            'phone': 'Телефон (в формате +7XXXXXXXXXX)',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'pattern': '\+7\d{10}'}),
        }
