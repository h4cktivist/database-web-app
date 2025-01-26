from django import forms

from .models import Halls


class HallsForm(forms.ModelForm):
    class Meta:
        model = Halls
        fields = ['name', 'capacity']
        labels = {
            'name': 'Название зала',
            'capacity': 'Вместимость',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 1}),
        }