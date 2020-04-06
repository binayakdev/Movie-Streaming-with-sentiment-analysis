from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('movies', views.movies, name='movies'),
    re_path(r'^watch_movies/movie_id=(?P<id>\d+)/$', views.watch_movies, name='watch_movies'),
    re_path(r'(?P<id>\d+)/favourite_movies/$', views.favourite_movie, name="favourite_movie"),
    path('favourites/list', views.list_favourites, name='list_favourites'),
    path('A-Z', views.chronological, name='chronological'),
    path('top_rated', views.top_rated, name='top_rated'),
    path('by_genre', views.by_genre, name='by_genre'),
    path('recent_releases', views.recent_releases, name='recent_releases'),
]

urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


