from django.test import TestCase, Client
from django.urls import reverse
from UserSettings.models import Profile
from movietime.models import Movie, Genre
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile


class MovieTimeModule(TestCase):

    def setUp(self):
        # self.client = Client()

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        self.user = Profile.objects.create_user(
            username='testuser',
            password='secret',
            first_name='first',
            last_name='last',
            email='test@gmail.com',
            bio='This is a test',
            avatar=SimpleUploadedFile(
                'small.gif', small_gif, content_type='image/gif')
        )

        self.genre = Genre.objects.create(
            genre_name='Action'
        )

        self.movie = Movie.objects.create(
            title='Avengers',
            poster=SimpleUploadedFile(
                'small.gif', small_gif, content_type='image/gif'),
            video=SimpleUploadedFile(
                'small.gif', small_gif, content_type='image/gif'),
            y_token='asaASS82si',
            cast='cast1, cast2',
            director='director',
            rating=8.5,
            duration='2h55m',
            quality='HD',
            release_date=datetime.datetime.now(),
            summary='This is a test',
            review_id='21asdkkkl'
        )

        self.movie.favourite.add(1)
        self.movie.genre.add(1)

    def test_movie_search_string_session(self):
        movie_string = 'Avengers'

        response = self.client.get('/movies', {'movies': movie_string})
        session = self.client.session
        self.assertEqual(session['search_query'], movie_string)
