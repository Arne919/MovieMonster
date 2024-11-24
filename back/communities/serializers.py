from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User  # 사용자 모델 가져오기


class ArticleListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()
    movie_id = serializers.IntegerField(source='movie.movie_id', read_only=True)  # 영화 ID
    movie_title = serializers.CharField(source='movie.title', read_only=True)  # 영화 제목
    poster_url = serializers.CharField(source='movie.poster_url', read_only=True)  # 포스터 URL
    movie_genres = serializers.SerializerMethodField()  # 장르 리스트
    movie_overview = serializers.CharField(source='movie.description', read_only=True)  # 영화 설명
    movie_rating = serializers.FloatField(source='movie.vote_avg', read_only=True)  # 영화 평점
    user_profile_image = serializers.SerializerMethodField()  # 사용자 프로필 이미지 추가
    is_liked = serializers.SerializerMethodField()  # 좋아요 상태 추가

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user in obj.like_users.all()  # 현재 사용자가 좋아요한 상태 반환

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'like_count', 'comment_count', 'poster_url',
            'user', 'user_profile_image', 'rating', 'created_at', 'updated_at', 'movie_id', 'movie_title',
            'movie_genres', 'movie_overview', 'movie_rating', 'is_liked',
        )

    def get_movie_genres(self, obj):
        if obj.movie and obj.movie.genres:
            return obj.movie.genres.split(',')  # 문자열로 저장된 장르를 리스트로 변환
        return []
    
    def get_user_profile_image(self, obj):
        user = obj.user
        if hasattr(user, 'get_profile_picture_url'):
            return user.get_profile_picture_url()
        return '/media/default-profile.png'  # 기본값



class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수 추가
    user = serializers.StringRelatedField()
    movie_title = serializers.CharField(source='movie.title', read_only=True)  # 영화 제목
    movie_poster_url = serializers.CharField(source='movie.poster_url', read_only=True)  # 영화 포스터
    movie_genres = serializers.SerializerMethodField()  # 영화 장르 리스트
    movie_rating = serializers.FloatField(source='movie.vote_avg', read_only=True)  # 영화 평점
    movie_overview = serializers.CharField(source='movie.description', read_only=True)  # 영화 설명
    is_liked = serializers.SerializerMethodField()  # 좋아요 상태 추가

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user in obj.like_users.all()  # 현재 사용자가 좋아요한 상태 반환

    def get_movie_genres(self, obj):
        """
        movie.genres가 쉼표로 구분된 문자열이라면 리스트로 변환.
        """
        if obj.movie and obj.movie.genres:
            return obj.movie.genres.split(", ")
        return []
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'movie_title', 'movie_poster_url', 'movie_genres', 'movie_rating', 'movie_overview')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 댓글 작성자 이름을 문자열로 반환

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'created_at')  # 댓글 ID, 작성자, 내용, 작성시간 반환

class RankingSerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField()  # 게시물 수
    likes_count = serializers.IntegerField()  # 좋아요 수
    followers_count = serializers.IntegerField()  # 팔로워 수

    class Meta:
        model = User
        fields = ('id', 'username', 'points', 'articles_count', 'likes_count', 'followers_count')
