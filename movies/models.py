from django.db import models

from django.contrib.auth.models import User

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # view, like
    timestamp = models.DateTimeField(auto_now_add=True)


class Movie(models.Model):
    movieId = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    genres = models.TextField()

    def __str__(self):
        return self.title
