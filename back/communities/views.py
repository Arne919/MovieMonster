from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Count

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        # 수정: get_list_or_404를 사용하지 않고 all()을 사용하여 모든 게시글을 가져옴
        articles = Article.objects.annotate(comment_count=Count('comments')).all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = get_list_or_404(Article.objects.annotate(comment_count=Count('comments')))
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         # 인증된 사용자만 게시글을 작성할 수 있도록 설정
#         if not request.user.is_authenticated:
#             return Response({"error": "인증된 사용자만 게시글을 작성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 요청자가 작성자인지 확인
        if request.user != article.user:
            return Response({"error": "본인의 게시글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 수정 처리
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def delete_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    # 요청한 사용자가 게시글 작성자인지 확인
    if request.user != article.user:
        return Response({"error": "본인의 게시글만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    article.delete()  # 게시글 삭제
    return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    if user in article.like_users.all():
        article.like_users.remove(user)  # 이미 좋아요한 경우 취소
        action = 'removed'
    else:
        article.like_users.add(user)  # 좋아요 추가
        action = 'added'

    article.save()
    return Response({
        'like_count': article.like_count(),
        'action': action
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)  # 게시글을 찾음

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)  # 현재 사용자와 게시글을 연결하여 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_comments(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)  # 게시글을 찾음
    comments = article.comments.all()  # 해당 게시글에 대한 댓글 가져오기
    serializer = CommentSerializer(comments, many=True)  # 댓글 목록 직렬화
    return Response(serializer.data)  # 댓글 목록 반환