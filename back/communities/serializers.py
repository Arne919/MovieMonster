from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수 추가
    user = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'like_count', 'comment_count', 'poster_url', 'user', 'rating' )


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