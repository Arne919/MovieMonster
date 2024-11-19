from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/like/', views.like_article, name='like-article'),
    path('articles/<int:article_pk>/comments/', views.create_comment, name='create-comment'),
]