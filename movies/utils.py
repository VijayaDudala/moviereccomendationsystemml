from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie

def get_recommendations(movie_id, n=5):

    movies = Movie.objects.all()
    
    movie_data = [
        {
            'movieId': movie.movieId,
            'title': movie.title,
            'genres': movie.genres
        }
        for movie in movies
    ]

    import pandas as pd
    df = pd.DataFrame(movie_data)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['genres'].fillna(''))

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    idx = df[df['movieId'] == movie_id].index[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:n+1]
    movie_indices = [i[0] for i in sim_scores]

    return df.iloc[movie_indices]