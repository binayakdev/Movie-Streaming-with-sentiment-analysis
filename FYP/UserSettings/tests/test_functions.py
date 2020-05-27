from django.test import TestCase, Client
from django.urls import reverse
from UserSettings.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile


class UserSettingsModule(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        self.wrong_credentials = {
            'username': 'testuser',
            'password': 'scret'
        }

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        Profile.objects.create_user(
            username='testuser',
            password='secret',
            first_name='first',
            last_name='last',
            email='test@gmail.com',
            bio='This is a test',
            avatar=SimpleUploadedFile(
                'small.gif', small_gif, content_type='image/gif')
        )
        self.client = Client()

    # Testing the login with invalid data
    def test_login_function_invalid(self):
        print("\nTesting the login function with invalid data..\n")
        # send login data
        response = self.client.post(
            '/accounts/login/', self.wrong_credentials, follow=True)
        # should be logged in now
        self.assertFalse(response.context['user'].is_authenticated)

    # Testing the login with valid data

    def test_login_function(self):
        print("\nTesting the login function..\n")
        # send login data
        response = self.client.post(
            '/accounts/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)
