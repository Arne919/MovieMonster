from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True) # 장르 이름
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)  # 영화 제목
    poster_url = models.URLField(max_length=500) # 포스터 URL
    genres = models.ManyToManyField(Genre, related_name="movies")  # 다대다 관계
    release_date = models.DateField()  # 실제 개봉일 저장
    director = models.CharField(max_length=100)  # 감독 이름
    actors = models.TextField()  # 주요 배우 (콤마로 구분된 문자열로 저장 가능)
    description = models.TextField()  # 영화 설명
    trailer_url = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.title
      