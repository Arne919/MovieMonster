from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from .models import User, Category, Ranking, Game
from .serializers import UserSerializer, CategorySerializer, MovieSerializer, RankingSerializer, GameSerializer, ProfileSerializer, UserRankSerializer

from django.middleware.csrf import get_token

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    user = request.user
    name = request.data.get('name')

    if not name or not name.strip():
        return Response({'error': 'Category name cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

    if Category.objects.filter(user=user, name=name).exists():
        return Response({'error': 'Category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.create(user=user, name=name.strip())
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Failed to create category: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from movies.models import Movie
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie_to_category(request):
    user = request.user
    category_id = request.data.get('category_id')
    movie_id = request.data.get('movie_id')

    if not category_id or not movie_id:
        return Response(
            {'error': 'category_id와 movie_id는 필수 항목입니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        category = Category.objects.get(id=category_id, user=user)
    except Category.DoesNotExist:
        return Response(
            {'error': '해당 카테고리를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(
            {'error': '해당 영화를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # ManyToManyField 또는 Custom 관계 추가
    category.movies.add(movie)

    return Response(
        {'message': f'영화 "{movie.title}"가 카테고리 "{category.name}"에 추가되었습니다.'},
        status=status.HTTP_200_OK,
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail(request, category_id):
    """
    특정 카테고리의 상세 정보 및 연결된 영화 반환
    """
    try:
        # 요청한 유저 소유의 카테고리인지 확인
        category = Category.objects.get(id=category_id, user=request.user)
    except Category.DoesNotExist:
        return Response({'error': '해당 카테고리를 찾을 수 없습니다.'}, status=404)

    # 카테고리에 연결된 영화 가져오기
    movies = category.movies.all()
    movie_serializer = MovieSerializer(movies, many=True)
    return Response({
        'id': category.id,
        'name': category.name,
        'movies': movie_serializer.data,  # 영화 데이터 포함
    }, status=200)




# 사용자 프로필 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 사용자 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])  # POST와 GET 모두 지원
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_points(request):
    user = request.user  # 현재 로그인한 유저

    if request.method == 'POST':
        # 프론트에서 받은 추가 점수 처리
        points_to_add = request.data.get('points', 0)
        user.points += points_to_add
        user.save()
        return Response(
            {
                'message': 'Points updated successfully!',
                'username': user.username,
                'current_points': user.points
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'GET':
        # 유저 정보 반환
        return Response(
            {
                'username': user.username,
                'current_points': user.points
            },
            status=status.HTTP_200_OK
        )
        
from communities.models import Article  # Article 모델 임포트

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    # 사용자 객체 가져오기
    user = get_object_or_404(User, username=username)

    # 해당 유저의 카테고리 가져오기
    categories = Category.objects.filter(user=user)
    category_serializer = CategorySerializer(categories, many=True)

    # 게시글 수와 좋아요 수 계산
    articles_count = Article.objects.filter(user=user).count()
    likes_count = Article.objects.filter(user=user).aggregate(
        total_likes=Count('like_users')
        )['total_likes'] or 0
    
    return Response({
        'id': user.id,
        'username': user.username,
        'points': user.points,  # 포인트
        'followers_count': user.followers.count(),  # 팔로워 수
        'followings_count': user.followings.count(),  # 팔로잉 수
        'articles_count': articles_count,  # 작성한 게시글 수
        'likes_count': likes_count,  # 총 좋아요 수
        'is_followed': request.user in user.followers.all(),  # 현재 사용자가 팔로우 중인지 여부
        'categories': category_serializer.data,  # 유저 카테고리 포함
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            is_followed = False
        else:
            person.followers.add(user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', person.username)


from django.middleware.csrf import get_token

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})
