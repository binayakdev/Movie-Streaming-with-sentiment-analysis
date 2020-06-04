from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from .models import Movie, Genre, FAQ
from UserSettings.models import SubscriptionPlan
from django.db.models import Q
from django.shortcuts import get_object_or_404

genres = None

# Create your views here.

'''
This is the python decorator that checks is the user is authenticated or not.
'''


def user_login_required(f):
    def wrap(request, *args, **kwargs):
        # This check the session if the userid key exists, if not it will redirect to login page
        if '_auth_user_id' not in request.session.keys():
            print("Session???")
            return redirect('login')

        if '_auth_user_id' in request.session.keys() and request.user.is_superuser:
            print("Not staff")
            return redirect('login')

        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


# This function renders the home page of the website
def index(request):
    context = {
        'title': 'MovieTime: Watch your favorite movies and also analyze the movies with sentiment analysis',
    }
    return render(request, 'movietime/index.html', context)


# This function renders the about page of the website
def about(request):
    faqs = FAQ.objects.all()

    free_plan = SubscriptionPlan.objects.get(membership_type='Free')
    premium_plan = SubscriptionPlan.objects.get(membership_type='Premium')

    print(free_plan)

    context = {
        'title': 'MovieTime: How it works',
        'faqs': faqs,
        'free_plan': free_plan,
        'premium_plan': premium_plan,
    }
    return render(request, 'movietime/about.html', context)


'''
This function uses the Django pagination
It takes in a list of movies object and seperates the content in the webpage into discrete pages
It returns the pages.
'''


def pagination(request, movie_list):
    paginator = Paginator(movie_list, 18)
    page = request.GET.get('page')
    return paginator.get_page(page)


'''
This functions checks if the list of movies are bookmarked
If a movies is bookmarked the movie id is appended to a list and returned
'''


def is_bookmarked(request, movies):
    bookmarked = []
    if request.user:
        for movie in movies:
            if movie.favourite.filter(id=request.user.id).exists():
                bookmarked.append(movie.id)
    return bookmarked

# This functions renders the movie details page


def movies(request):
    movies = None
    random_movies = None
    favourites = []
    if request.method == 'GET' and 'page' not in request.GET:
        search_query = request.GET['movies'].strip()
        request.session['search_query'] = search_query
    if request.session['search_query'] == "":
        movies = Movie.objects.all()
    else:
        movies = Movie.objects.filter(
            Q(title__icontains=request.session['search_query']))

    if not movies:
        random_movies = Movie.objects.raw(
            'SELECT * FROM movietime_movie WHERE id IN (SELECT id FROM (SELECT id FROM movietime_movie ORDER BY RAND() LIMIT 10) t)'
        )
    else:
        favourites = is_bookmarked(request, movies)

    genres = Genre.objects.all()

    movie_list = pagination(request, movies)

    context = {
        'title': 'MovieTime: ' + request.session['search_query'],
        'query': request.session['search_query'],
        'movies': movie_list,
        'suggestions': random_movies,
        'favourites': favourites,
        'genres': genres,
    }
    return render(request, 'movietime/movies.html', context)


# This functions returns the watch movie webpage
# This is where the users streams their movie
# The user needs to be authenticated in order to access this page.
@user_login_required
def watch_movies(request, id):
    movie = Movie.objects.get(id=id)
    casts = movie.cast.split(", ")
    directors = movie.director.split(", ")
    is_bookmarked = False

    if movie.favourite.filter(id=request.user.id).exists():
        is_bookmarked = True

    context = {
        'title': movie.title,
        'movie': movie,
        'casts': casts,
        'directors': directors,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'movietime/watch_movies.html', context)

#  This function filters the movies by the recent release date


def recent_releases(request):
    movies = Movie.objects.all().order_by('-release_date')
    recent_releases = pagination(request, movies)
    favourites = is_bookmarked(request, movies)

    context = {
        'title': 'MovieTime: Recent Releases',
        'query': 'Recent Releases',
        'movies': recent_releases,
        'favourites': favourites,
        'genres': Genre.objects.all()
    }
    return render(request, 'movietime/movies.html', context)

# This functions filters the movies in a chornological order (i.e. from A to Z)


def chronological(request):
    movies = Movie.objects.all().order_by('title')
    chronological_movies = pagination(request, movies)
    favourites = is_bookmarked(request, movies)

    context = {
        'title': 'MovieTime: A-Z',
        'query': 'A-Z',
        'movies': chronological_movies,
        'favourites': favourites,
        'genres': Genre.objects.all()
    }
    return render(request, 'movietime/movies.html', context)


# This functions filters the movies by their rating (hightest rated to lowest)
def top_rated(request):
    movies = Movie.objects.all().order_by('-rating')
    top_rated_movies = pagination(request, movies)
    favourites = is_bookmarked(request, movies)

    context = {
        'title': 'MovieTime: Top rated',
        'query': 'Top Rated',
        'movies': top_rated_movies,
        'favourites': favourites,
        'genres': Genre.objects.all()
    }
    return render(request, 'movietime/movies.html', context)

# This functions returns all the movies that falls on the selected genre category


def by_genre(request):
    if request.method == 'GET' and 'page' not in request.GET:
        genres = request.GET.getlist('checks')
        request.session['genres'] = genres

        if not genres:
            messages.info(
                request, f'You have to select at least one genre to filter the movies', extra_tags="Error")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    movies = Movie.objects.filter(
        genre__id__in=request.session['genres']).distinct()
    movies_by_genre = pagination(request, movies)
    favourites = is_bookmarked(request, movies)

    context = {
        'title': 'MovieTime: Genres',
        'query': 'By Genre',
        'movies': movies_by_genre,
        'favourites': favourites,
        'genres': Genre.objects.all(),
    }

    return render(request, 'movietime/movies.html', context)


# This functions adds the movie to the favourite list
# This function is called asynchronously using AJAX
# It returns JSON response containing a message.
@user_login_required
def favourite_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    data = {
        'success': False,
        'messsage': '',
    }
    if movie.favourite.filter(id=request.user.id).exists():
        movie.favourite.remove(request.user)
        data['message'] = "Movie removed from list"
    else:
        movie.favourite.add(request.user)
        data['message'] = "Movie added to list"
    data['success'] = True
    return JsonResponse(data, safe=False)

# This function renders the page that shows all the favourite movies of the authenticated user.
@user_login_required
def list_favourites(request):
    movies = Movie.objects.all()
    favourites = is_bookmarked(request, movies)
    favourite_movies = Movie.objects.filter(id__in=favourites).distinct()
    movie_list = pagination(request, favourite_movies)

    context = {
        'title': 'Your favourite list',
        'movies': favourite_movies,
    }

    return render(request, 'movietime/favourites.html', context)
