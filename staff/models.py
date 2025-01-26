from django.db import models


class Positions(models.Model):
    position_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Position'
        db_table = 'positions'

    def __str__(self):
        return f'{self.title}'


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    middle_name = models.TextField()
    position = models.ForeignKey(Positions, models.SET_NULL, null=True)
    phone = models.TextField()

    class Meta:
        ordering = ['first_name', 'last_name', 'middle_name']
        verbose_name = 'Staff'
        db_table = 'staff'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'
