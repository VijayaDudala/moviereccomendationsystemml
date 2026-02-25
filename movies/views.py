from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Movie, UserInteraction
from .serializers import MovieSerializer
from .utils import get_recommendations


# 🎬 API 1 — Get All Movies (Homepage)
@api_view(['GET'])
def get_movies(request):

    movies = Movie.objects.all()[:200]

    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)



# 🎬 API 2 — Click Movie → Get Recommendations
@api_view(['GET'])
def recommend_movie(request, movie_id):

    try:
        movie = Movie.objects.get(movieId=movie_id)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)

    # 👤 Save User Interaction
    if request.user.is_authenticated:
        UserInteraction.objects.get_or_create(
            user=request.user,
            movie=movie
        )

    # 🤖 Get ML Recommendations
    recommended = get_recommendations(movie_id)

    if len(recommended) == 0:
        return Response([])

    rec_ids = recommended['movieId'].tolist()

    movies = Movie.objects.filter(movieId__in=rec_ids)

    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)



# 👤 API 3 — Personalized Recommendations
@api_view(['GET'])
def user_recommendations(request):

    if not request.user.is_authenticated:
        return Response([])

    interactions = UserInteraction.objects.filter(user=request.user)

    if not interactions.exists():
        movies = Movie.objects.all()[:10]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    watched_ids = [i.movie.movieId for i in interactions]

    movies = Movie.objects.exclude(movieId__in=watched_ids)[:10]

    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)