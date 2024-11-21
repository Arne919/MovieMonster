from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import Count
from movies.models import Movie  # Movie 모델 참조

class User(AbstractUser):
    profile_picture = models.URLField(max_length=100, blank=True)
    points = models.IntegerField(default=500)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def sum_likes(self):
        """
        사용자가 작성한 게시글에 대한 총 좋아요 수를 반환
        """
        from communities.models import Article  # 순환 참조 방지
        return Article.objects.filter(user=self).aggregate(total_likes=Count('like_users'))['total_likes'] or 0

class Category(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class CategoryMovie(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_categories')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.movie.title}"

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
