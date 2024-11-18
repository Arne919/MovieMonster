from django.contrib import admin
from .models import Movie, Genre


# class MovieAdmin(admin.ModelAdmin):
#     list_display = ('title', 'genre', 'release_date', 'rating')  # 관리자 페이지 목록에 표시될 필드
#     search_fields = ('title', 'genre')  # 검색 가능한 필드
#     list_filter = ('genre', 'release_date')  # 필터 추가


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')  # 'genres'는 다대다 관계로 표시가 어려우므로 제거
    search_fields = ('title',)
    list_filter = ('release_date',)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)