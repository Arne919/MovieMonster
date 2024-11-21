from rest_framework import serializers
from .models import User, Category, Ranking, Game
from movies.models import Movie

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile_picture',
            'points',
            'follower',
            'following',
            'created_at',
        ]
class ProfileSerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(source='articles.count', read_only=True)  # 게시글 수
    likes_count = serializers.IntegerField(source='sum_likes', read_only=True)  # 총 좋아요 수

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'points',
            'follower',
            'following',
            'articles_count',
            'likes_count',  # sum_likes 매핑
        ]

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_url']
        
class CategorySerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True, source='category_movies.movie')

    class Meta:
        model = Category
        fields = ['id', 'name', 'movies']


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ['id', 'user', 'rank', 'week_start', 'week_end']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'user', 'game_type', 'score', 'created_at']

class UserRankSerializer(serializers.ModelSerializer):
    rank_title = serializers.SerializerMethodField()

    def get_rank_title(self, obj):
        print(f"User: {obj.username}, Points: {obj.points}")  # 디버깅용 로그
        if obj.points <= 1000:
            return "Bronze"
        elif obj.points <= 2000:
            return "Silver"
        elif obj.points <= 3000:
            return "Gold"
        elif obj.points <= 4000:
            return "Platinum"
        else:
            return "Diamond"

    class Meta:
        model = User
        fields = ['username', 'points', 'rank_title', 'articles_count', 'likes_count', 'followers_count']
