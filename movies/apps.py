from django.apps import AppConfig
import threading

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):

        def build_model():
            from .utils import build_recommendation_model
            build_recommendation_model()

        threading.Thread(target=build_model).start()