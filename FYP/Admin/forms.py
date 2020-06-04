from django import forms
from UserSettings.models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib import messages


# This the admin registration form
class UserAdminRegisterForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'username', 'email']

# This is the admin login form


class CustomAdminChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ('username', 'password')
        help_texts = {
            'username': None,
            'password': None,
        }

# This is the admin password reset form that asks for the email


class AdminPasswordResetForm(PasswordResetForm):

    class Meta:
        model = Profile
        fields = ('email',)


# This is the admin password reset form that asks for the new password
class AdminPasswordResetConfirmForm(SetPasswordForm):

    class Meta:
        model = Profile
        fields = ('password',)
