from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from UserSettings.forms import UserRegisterForm, CustomUserChangeForm, CustomUserEditForm


class TestForms(TestCase):

    def setUp(self):
        self.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

    def test_register_form_valid_data(self):
        print("\nTesting the register form with valid data...\n")

        form = UserRegisterForm(
            data={
                'first_name': 'Binayak',
                'last_name': 'Joshi',
                'username': 'DEV',
                'email': 'joshibinayak@gmail.com',
                'bio': 'I love movies!!',
                'password1': '&YXH}Tf>P#w5P)_H',
                'password2': '&YXH}Tf>P#w5P)_H',
            },
            files={
                'avatar': SimpleUploadedFile('small.gif', self.small_gif, content_type='image/gif')
            }
        )

        self.assertTrue(form.is_valid())

    def test_edit_form_valid_data(self):
        print("\nTesting the edit form with valid data..\n")

        form = CustomUserEditForm(data={
            'username': 'DEV',
            'first_name': 'Binayak',
            'last_name': 'Joshi',
            'email': 'joshibinayak17@gmail.com',
            'bio': 'This is a test'
        },
            files={
            'avatar': SimpleUploadedFile('small.gif', self.small_gif, content_type='image/gif')
        })

    def test_register_form_no_data(self):
        print("\nTesting the regsiter form with no data..\n")

        form = UserRegisterForm(data={}, files={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_login_form_no_data(self):
        print("\nTesting the login form with no data\n")

        form = CustomUserChangeForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_edit_form_no_data(self):
        print("\nTesting the edit form with no data...\n")

        form = UserRegisterForm(data={}, files={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)
