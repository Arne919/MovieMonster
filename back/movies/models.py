from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    popularity = models.FloatField(null=True, blank=True)
    vote_avg = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title