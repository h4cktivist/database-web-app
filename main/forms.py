from django import forms
from django.utils import timezone

from .models import Sales
from staff.models import Staff


class SalesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['ticket'].queryset = Tickets.objects.filter(pk=self.instance.ticket.pk) | Tickets.objects.exclude(
                session__in=Sales.objects.exclude(pk=self.instance.pk).values_list('ticket__session', flat=True)
            )
            self.fields['staff'].queryset = Staff.objects.filter(pk=self.instance.staff.pk) | Staff.objects.filter(position__title='Кассир')
        else:
            self.fields['ticket'].queryset = Tickets.objects.exclude(
                session__in=Sales.objects.all().values_list('ticket__session', flat=True)
            )
            self.fields['staff'].queryset = Staff.objects.filter(position__title='Кассир')

    def clean(self):
        cleaned_data = super().clean()
        sale_date = cleaned_data.get("date")
        if sale_date:
            if sale_date > timezone.now().date():
                raise forms.ValidationError("Дата продажи не может быть позже текущей даты.")
        return cleaned_data

    class Meta:
        model = Sales
        fields = ['ticket', 'staff', 'date', 'payment_type', 'customer']
        labels = {
            'ticket': 'Билет',
            'staff': 'Сотрудник',
            'date': 'Дата продажи',
            'payment_type': 'Тип оплаты',
            'customer': 'Покупатель',
        }
        PAYMENT_TYPES = [
            ('Наличные', 'Наличные'),
            ('Карта', 'Карта'),
        ]
        widgets = {
            'ticket': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'staff': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'payment_type': forms.Select(choices=PAYMENT_TYPES, attrs={'class': 'form-control', 'required': True}),
            'customer': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
