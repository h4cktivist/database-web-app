from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from movies.models import Movies
from halls.models import Halls


class SessionTypes(models.Model):
    session_type_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Session Type'
        db_table = 'session_types'

    def __str__(self):
        return f'{self.name}'


class Sessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_date = models.DateField()
    session_time = models.TimeField()
    session_type = models.ForeignKey(SessionTypes, models.SET_NULL, null=True)
    movie = models.ForeignKey(Movies, models.SET_NULL, null=True)
    hall = models.ForeignKey(Halls, models.SET_NULL, null=True)

    class Meta:
        ordering = ['session_date']
        verbose_name = 'Session'
        db_table = 'sessions'

    def __str__(self):
        return f'{self.session_date} {self.session_time} | {self.movie.title if self.movie is not None else ""} | {self.hall}'

    def clean(self):
        existing_sessions = Sessions.objects.filter(
            session_date=self.session_date,
            session_time=self.session_time,
            hall=self.hall,
        )
        if existing_sessions.exists() and self.pk != existing_sessions.first().pk:
            raise ValidationError(_("Сеанс на данное время, дату и зал уже существует."))
        super().clean()


class Tickets(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    price = models.FloatField()
    session = models.ForeignKey(Sessions, models.SET_NULL, null=True)
    row_number = models.IntegerField()
    seat_number = models.IntegerField()

    def __str__(self):
        return f'Сеанс {self.session.session_id} | {self.price} | {self.row_number}, {self.seat_number}'

    class Meta:
        ordering = ['ticket_id']
        verbose_name = 'Ticket'
        db_table = 'tickets'

    def clean(self):
        existing_sessions = Tickets.objects.filter(
            session=self.session,
            row_number=self.row_number,
            seat_number=self.seat_number,
        )
        if existing_sessions.exists() and self.pk != existing_sessions.first().pk:
            raise ValidationError(_("Билет на данный сеанс с таким местом уже сущестует."))
        super().clean()
