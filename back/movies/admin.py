from django.contrib import admin
from .models import Movie, Genre

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'rating')  # 관리자 페이지 목록에 표시될 필드
    search_fields = ('title', 'genre')  # 검색 가능한 필드
    list_filter = ('genre', 'release_date')  # 필터 추가

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
