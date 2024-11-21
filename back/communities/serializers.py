from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User  # 사용자 모델 가져오기


class ArticleListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수 추가
    user = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'like_count', 'comment_count', 'poster_url', 'user', 'rating', 'created_at', 'updated_at' )


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수 추가
    user = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user','like_users',)

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
