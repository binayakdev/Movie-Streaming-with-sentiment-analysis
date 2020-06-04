from django.db import models
import datetime

# Create your models here.

# This is Movie details table


class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters')
    video = models.FileField(upload_to='movies', null=True, verbose_name="")
    y_token = models.CharField(max_length=20)
    cast = models.CharField(max_length=200, default="Binayak")
    director = models.CharField(max_length=50, default="Binayak")
    rating = models.FloatField(default="0.0")
    duration = models.CharField(max_length=20, default="0h0m")
    quality = models.CharField(max_length=10, default="HD")
    release_date = models.DateField(default=datetime.date.today)
    summary = models.TextField(blank=False, default="Nothing")
    # This creates a many to many relation with the favourite table
    favourite = models.ManyToManyField(
        "UserSettings.Profile", related_name='favourite', blank=True)  # This creates a many to many relation with the User profile table
    genre = models.ManyToManyField("Genre", related_name='genre', blank=True)
    review_id = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Movie"

# This is the Genre table


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name_plural = "Genre"

# This is the FAQ table


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQ"
