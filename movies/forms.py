from django import forms

from .models import Movies


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
