from django.contrib import admin
from .models import Movie, Genre, FAQ

# Register your models here.
# Registering the Movie model to the superuser dashboard
admin.site.register(Movie)
# Registering the Genre model to the superuser dashboard
admin.site.register(Genre)
# Registering the FAQ model to the superuser dashboard
admin.site.register(FAQ)
