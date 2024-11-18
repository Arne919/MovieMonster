import os
import json
from django.http import JsonResponse
from django.views import View
from .models import Movie, Genre

# 모든 영화 조회
class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.all().values('id', 'title', 'poster_url')
        return JsonResponse(list(movies), safe=False)

# 특정 영화 상세 조회
# class MovieDetailView(View):
#     def get(self, request, movie_id):
#         try:
#             movie = Movie.objects.filter(id=movie_id).values(
#                 'id', 'title', 'poster_url', 'vote_avg', 'director',
#                 'release_date', 'description'
#             ).first()

#             if movie:
#                 # 배우 및 장르 추가
#                 genres = list(Movie.objects.get(id=movie_id).genres.values_list('name', flat=True))
#                 actors = list(Movie.objects.get(id=movie_id).actors.values_list('name', flat=True))
#                 movie['genres'] = genres
#                 movie['actors'] = actors


#                 return JsonResponse(movie)
#             else:
#                 return JsonResponse({'error': 'Movie not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
# JSON_FILE_PATH = "fixtures/movies/popular.json"
# -------------------------------------
from django.conf import settings  # BASE_DIR 사용

# JSON 파일 경로 설정
JSON_FILE_PATH = os.path.join(settings.BASE_DIR, "movies", "fixtures", "movies", "movie_data.json")

class MovieDetailView(View):
    def get(self, request, movie_id):
        try:
            # JSON 파일 열기
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            # 요청된 movie_id에 해당하는 영화 검색
            for entry in data:
                fields = entry["fields"]
                if fields["movie_id"] == movie_id:
                    # 영화 데이터 구성
                    movie = {
                        "id": fields["movie_id"],
                        "title": fields["title"],
                        "poster_url": fields["poster_url"],
                        "vote_avg": fields["vote_avg"],
                        "director": fields["director"],
                        "release_date": fields["release_date"],
                        "description": fields["description"],
                        "genres": fields["genres"],  # 리스트 그대로 반환
                        "actors": fields["actors"],  # 리스트 그대로 반환
                    }
                    return JsonResponse(movie)

            # 해당 movie_id를 찾을 수 없는 경우
            return JsonResponse({"error": "Movie not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# 장르별 영화 조회
class MoviesByGenreView(View):
    def get(self, request, genre_name):
        try:
            genre = Genre.objects.get(name=genre_name)
            movies = genre.movies.all().values('id', 'title', 'release_date', 'poster_url', 'description')
            return JsonResponse(list(movies), safe=False)
        except Genre.DoesNotExist:
            return JsonResponse({'error': 'Genre not found'}, status=404)
