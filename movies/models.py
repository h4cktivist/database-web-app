from django.db import models


class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.TextField()
    genre = models.TextField()
    duration = models.IntegerField()
    age_restriction = models.TextField()
    rating = models.FloatField()
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name = 'Movie'
        db_table = 'movies'

    def __str__(self):
        return f'{self.title} | {self.genre}'
