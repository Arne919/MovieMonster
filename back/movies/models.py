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
    movie_id = models.IntegerField(unique=True)  # JSON 파일의 movie_id
    title = models.CharField(max_length=255)  # 영화 제목
    release_date = models.DateField()  # 개봉일
    popularity = models.FloatField(null=True, blank=True)  # 인기 점수
    vote_avg = models.FloatField(null=True, blank=True)  # 평균 평점
    description = models.TextField(blank=True, null=True)  # 설명
    poster_url = models.URLField(max_length=500, blank=True, null=True)  # 포스터 URL
    genres = models.TextField()
    actors = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)  # 감독 이름

    def __str__(self):
        return self.title
