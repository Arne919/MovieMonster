from django.urls import path, include
from . import views

urlpatterns = [
    # path('register/', views.register_user, name='register_user'),
    # path('login/', views.login_user, name='login_user'),
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 패스워드 변경 등
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입 관련 URL
    # path('profile/', views.get_user_profile, name='get_user_profile'),
    path("profile/<username>/", views.profile, name="profile"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path('users/', views.get_users, name='get_users'),
    path('categories/', views.get_categories, name='get_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/add-movie/', views.add_movie_to_category, name='add_movie_to_category'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    # path('rankings/', views.get_user_rankings, name='get_user_rankings'),
    # path('games/', views.manage_games, name='manage_games'),
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('user/points/', views.user_points, name='user_points'),
]
