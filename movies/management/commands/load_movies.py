from django.core.management.base import BaseCommand
from movies.models import Movie
import pandas as pd


class Command(BaseCommand):
    help = "Load movies from MovieLens dataset"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("ml-latest-small/movies.csv")

        count = 0
        for _, row in df.iterrows():
            Movie.objects.get_or_create(
                movieId=row['movieId'],
                title=row['title'],
                genres=row['genres']
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} movies imported successfully!"))
