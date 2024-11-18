from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('users/', views.get_users, name='get_users'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('rankings/', views.get_user_rankings, name='get_user_rankings'),
    path('games/', views.manage_games, name='manage_games'),
]
