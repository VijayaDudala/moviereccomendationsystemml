import pickle
import os
from django.conf import settings
from .models import Movie
from collections import defaultdict
from .models import UserInteraction

BASE_DIR = settings.BASE_DIR

cosine_sim = pickle.load(open(os.path.join(BASE_DIR, 'movies/cosine_sim.pkl'), 'rb'))
movies_df = pickle.load(open(os.path.join(BASE_DIR, 'movies/movies_df.pkl'), 'rb'))


def get_recommendations(movie_id, n=5):
    idx = movies_df[movies_df['movieId'] == movie_id].index[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    return movies_df.iloc[movie_indices]


def get_user_recommendations(user, n=10):
    interactions = UserInteraction.objects.filter(user=user)

    if not interactions.exists():
        return []

    score_dict = defaultdict(int)

    for interaction in interactions:
        recs = get_recommendations(interaction.movie.movieId, n=5)
        
        for _, movie in recs.iterrows():
            score_dict[movie['movieId']] += 1

    sorted_movies = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    top_movie_ids = [movie_id for movie_id, _ in sorted_movies[:n]]

    return Movie.objects.filter(movieId__in=top_movie_ids)