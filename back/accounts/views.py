from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import User, Category, Ranking, Game
from .serializers import UserSerializer, CategorySerializer, RankingSerializer, GameSerializer

from django.middleware.csrf import get_token

# 회원가입
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     data = request.data
#     serializer = UserSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save(password=make_password(data['password']))
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 로그인
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         csrf_token = get_token(request)
#         return Response({
#             "message": "Login successful!",
#              "csrf_token": csrf_token
#              }, status=status.HTTP_200_OK)
#     else:
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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

# 카테고리 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_categories(request):
    if request.method == 'GET':
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 사용자 랭킹 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rankings(request):
    rankings = Ranking.objects.filter(user=request.user)
    serializer = RankingSerializer(rankings, many=True)
    return Response(serializer.data)

# 게임 기록 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_games(request):
    if request.method == 'GET':
        games = Game.objects.filter(user=request.user)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return Response({
        'id': user.id,
        'username': user.username,
        'points': user.points,  # 포인트 추가
        'followers_count': user.followers.count(),
        'followings_count': user.followings.count(),
        'is_followed': request.user in user.followers.all(),
    })

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def profile(request, username):
#     User = get_user_model()
#     person = User.objects.get(username=username)
#     context = {
#         "person": person,
#     }
#     return render(request, "accounts/profile.html", context)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def follow(request, user_pk):
#     person = get_object_or_404(User, pk=user_pk)
#     user = request.user

#     if person != user:
#         if person.followers.filter(pk=user.pk).exists():
#             person.followers.remove(user)
#             is_followed = False
#         else:
#             person.followers.add(user)
#             is_followed = True

#         return Response({
#             'is_followed': is_followed,
#             'followings_count': person.followings.count(),
#             'followers_count': person.followers.count(),
#         })

#     return Response({'error': 'You cannot follow yourself.'}, status=400)
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
