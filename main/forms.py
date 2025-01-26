from datetime import datetime

from django import forms
from django.utils import timezone

from .models import SessionTypes, Sessions, Tickets, Sales
from staff.models import Staff


class SessionTypesForm(forms.ModelForm):
    class Meta:
        model = SessionTypes
        fields = ['name']
        labels = {
            'name': 'Название типа сеанса',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class SessionsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        session_date = cleaned_data.get("session_date")
        session_time = cleaned_data.get("session_time")

        if session_date and session_time:
            session_datetime = timezone.make_aware(datetime.combine(session_date, session_time), timezone.get_current_timezone())
            if session_datetime < timezone.now():
                raise forms.ValidationError("Дата и время сеанса не могут быть раньше текущего времени.")
        return cleaned_data

    class Meta:
        model = Sessions
        fields = ['session_date', 'session_time', 'session_type', 'movie', 'hall']
        labels = {
            'session_date': 'Дата сеанса',
            'session_time': 'Время сеанса',
            'session_type': 'Тип сеанса',
            'movie': 'Фильм',
            'hall': 'Зал',
        }
        widgets = {
            'session_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'session_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
            'session_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'movie': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'hall': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }


class TicketsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session'].queryset = Sessions.objects.exclude(hall=None)
    class Meta:
        model = Tickets
        fields = ['price', 'session', 'row_number', 'seat_number']
        labels = {
            'price': 'Цена',
            'session': 'Сеанс',
            'row_number': 'Номер ряда',
            'seat_number': 'Номер места',
        }
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 0}),
            'session': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'row_number': forms.Select(attrs={'class': 'form-control row-select', 'required': True, 'min': 1}),
            'seat_number': forms.Select(choices=[(i, i) for i in range(1, 21)], attrs={'class': 'form-control seat-select', 'required': True, 'min': 1}),
        }


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
