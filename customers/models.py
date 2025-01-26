from django.db import models


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField()
    email = models.TextField()

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Customer'
        db_table = 'customers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
