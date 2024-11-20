from django.urls import path, include
from . import views

urlpatterns = [
    # path('register/', views.register_user, name='register_user'),
    # path('login/', views.login_user, name='login_user'),
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 패스워드 변경 등
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입 관련 URL
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('users/', views.get_users, name='get_users'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('rankings/', views.get_user_rankings, name='get_user_rankings'),
    path('games/', views.manage_games, name='manage_games'),
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('user/points/', views.user_points, name='user_points'),
]
