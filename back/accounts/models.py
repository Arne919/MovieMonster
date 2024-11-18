from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.URLField(max_length=100, blank=True)
    points = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Ranking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rankings')
    rank = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    game_type = models.CharField(max_length=50)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
