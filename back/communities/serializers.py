from rest_framework import serializers
from .models import Article


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
