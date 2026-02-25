from django.urls import path
from .views import get_movies, recommend_movie, user_recommendations

urlpatterns = [
    path('movies/', get_movies),
    path('recommend/<int:movie_id>/', recommend_movie),
    path('user-recommend/', user_recommendations),
]