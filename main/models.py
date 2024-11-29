# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField()
    email = models.TextField()

    class Meta:
        ordering = ['customer_id']
        verbose_name = 'Customer'
        db_table = 'customers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Halls(models.Model):
    hall_id = models.AutoField(primary_key=True)
    name = models.TextField()
    capacity = models.IntegerField()

    class Meta:
        ordering = ['hall_id']
        verbose_name = 'Hall'
        db_table = 'halls'

    def __str__(self):
        return f'{self.name}'


class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.TextField()
    genre = models.TextField()
    duration = models.IntegerField()
    age_restriction = models.TextField()
    rating = models.FloatField()
    description = models.TextField()

    class Meta:
        ordering = ['movie_id']
        verbose_name = 'Movie'
        db_table = 'movies'

    def __str__(self):
        return f'{self.title} | {self.genre}'


class Positions(models.Model):
    position_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['position_id']
        verbose_name = 'Position'
        db_table = 'positions'

    def __str__(self):
        return f'{self.title}'


class Sales(models.Model):
    sale_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey('Tickets', models.SET_NULL, null=True)
    staff = models.ForeignKey('Staff', models.SET_NULL, null=True)
    date = models.DateField()
    payment_type = models.TextField()
    customer = models.ForeignKey(Customers, models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Sale'
        db_table = 'sales'

    def __str__(self):
        return f'Продажа {self.sale_id} | {self.ticket.price if self.ticket is not None else ""} руб.'

    def clean(self):
        existing_sessions = Sales.objects.filter(
            ticket=self.ticket,
        )
        if existing_sessions.exists() and self.pk != existing_sessions.first().pk:
            raise ValidationError(_("Данный билет уже продан."))
        super().clean()


class SessionTypes(models.Model):
    session_type_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['session_type_id']
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
        ordering = ['-session_date']
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


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    middle_name = models.TextField()
    position = models.ForeignKey(Positions, models.SET_NULL, null=True)
    phone = models.TextField()

    class Meta:
        ordering = ['staff_id']
        verbose_name = 'Staff'
        db_table = 'staff'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'


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
