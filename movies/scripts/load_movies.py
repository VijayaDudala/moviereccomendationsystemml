import pandas as pd
from movies.models import Movie

def run():

    if Movie.objects.exists():
        print("Movies already loaded")
        return

    df = pd.read_csv("ml-latest-small/movies.csv")

    for _, row in df.iterrows():
        Movie.objects.create(
            movieId=row['movieId'],
            title=row['title'],
            genres=row['genres']
        )

    print("Movies loaded successfully!")