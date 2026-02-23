from django.shortcuts import render, get_object_or_404
from .models import Movie
from .utils import get_recommendations, get_user_recommendations    
from .models import UserInteraction

def movie_list(request):
    movies = Movie.objects.all()[:100]  # show first 100
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movieId=movie_id)

    if request.user.is_authenticated:
        UserInteraction.objects.create(
            user=request.user,
            movie=movie,
            interaction_type='view'
        )

    recommendations = get_recommendations(movie.movieId)

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'recommendations': recommendations
    })


def movie_list(request):
    movies = Movie.objects.all()[:100]

    personalized = []

    if request.user.is_authenticated:
        personalized = get_user_recommendations(request.user)

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'personalized': personalized
    })