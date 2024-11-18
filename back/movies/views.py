from django.http import JsonResponse
from django.views import View
from .models import Movie, Genre

# 모든 영화 조회
class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.all().values('id', 'title', 'genre', 'release_date', 'poster_url', 'rating')
        return JsonResponse(list(movies), safe=False)

# 특정 영화 상세 조회
class MovieDetailView(View):
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.filter(id=movie_id).values('id', 'title', 'genre', 'release_date', 'overview', 'poster_url', 'rating').first()
            if movie:
                return JsonResponse(movie)
            else:
                return JsonResponse({'error': 'Movie not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# 장르별 영화 조회
class MoviesByGenreView(View):
    def get(self, request, genre_name):
        movies = Movie.objects.filter(genre=genre_name).values('id', 'title', 'release_date', 'poster_url', 'rating')
        return JsonResponse(list(movies), safe=False)
