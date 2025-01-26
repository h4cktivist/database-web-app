from django.db import models


class Halls(models.Model):
    hall_id = models.AutoField(primary_key=True)
    name = models.TextField()
    capacity = models.IntegerField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Hall'
        db_table = 'halls'

    def __str__(self):
        return f'{self.name}'
