# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from customers.models import Customers
from movies.models import Movies
from halls.models import Halls
from staff.models import Staff
from sessions_tickets.models import Tickets


class Sales(models.Model):
    sale_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Tickets, models.SET_NULL, null=True)
    staff = models.ForeignKey(Staff, models.SET_NULL, null=True)
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
