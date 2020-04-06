from django import forms
from UserSettings.models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib import messages


class UserAdminRegisterForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'username', 'email']


class CustomAdminChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ('username', 'password')
        help_texts = {
            'username': None,
            'password': None,
        }


class AdminPasswordResetForm(PasswordResetForm):

    class Meta:
        model = Profile
        fields = ('email',)


class AdminPasswordResetConfirmForm(SetPasswordForm):

    class Meta:
        model = Profile
        fields = ('password',)
