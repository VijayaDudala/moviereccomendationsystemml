from django.contrib import admin
from .models import Movie


from .models import UserInteraction

admin.site.register(UserInteraction)


admin.site.register(Movie)
# Register your models here.
