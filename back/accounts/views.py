from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import User, Category, Ranking, Game
from .serializers import UserSerializer, CategorySerializer, RankingSerializer, GameSerializer
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save(password=make_password(data['password']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        csrf_token = get_token(request)
        return Response({
            "message": "Login successful!",
             "csrf_token": csrf_token
             }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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

from django.middleware.csrf import get_token

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})
