from django.test import SimpleTestCase
from django.urls import reverse, resolve
from movietime.views import index, about, movies, watch_movies, recent_releases, chronological, top_rated, by_genre, list_favourites


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        print("\nTesting the URLs for movietime app...\n")
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_about_url_is_resolved(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, about)

    def test_movies_url_is_resolved(self):
        url = reverse('movies')
        self.assertEquals(resolve(url).func, movies)

    def test_watch_movies_url_is_resolved(self):
        url = reverse('watch_movies', args=[1])
        self.assertEquals(resolve(url).func, watch_movies)

    def test_recent_releases_is_resolved(self):
        url = reverse('recent_releases')
        self.assertEquals(resolve(url).func, recent_releases)

    def test_chronological_url_is_resolved(self):
        url = reverse('chronological')
        self.assertEquals(resolve(url).func, chronological)

    def test_top_rated_url_is_resolved(self):
        url = reverse('top_rated')
        self.assertEquals(resolve(url).func, top_rated)

    def test_by_genre_url_is_resolved(self):
        url = reverse('by_genre')
        self.assertEquals(resolve(url).func, by_genre)
