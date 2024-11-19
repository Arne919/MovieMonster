from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'like_count')


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 댓글 작성자 이름을 문자열로 반환

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'created_at')  # 댓글 ID, 작성자, 내용, 작성시간 반환