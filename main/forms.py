from datetime import datetime

from django import forms
from django.utils import timezone
from .models import Customers, Halls, Movies, Positions, SessionTypes, Staff, Sessions, Tickets, Sales


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


class MoviesForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'genre', 'duration', 'age_restriction', 'rating', 'description']
        labels = {
            'title': 'Название фильма',
            'genre': 'Жанр',
            'duration': 'Продолжительность (мин)',
            'age_restriction': 'Возрастное ограничение (в формате X+)',
            'rating': 'Рейтинг',
            'description': 'Описание',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 1}),
            'age_restriction': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 0, 'max': 10}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
        }


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
            'session_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'session_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
            'session_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'movie': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'hall': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }


class TicketsForm(forms.ModelForm):
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
            'row_number': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 1}),
            'seat_number': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 1}),
        }


class SalesForm(forms.ModelForm):
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
        widgets = {
            'ticket': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'staff': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'payment_type': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'customer': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
