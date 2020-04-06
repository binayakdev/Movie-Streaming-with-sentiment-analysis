from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from django.forms import TextInput, Textarea
from django.core.exceptions import ValidationError
from django.contrib import messages


class UserRegisterForm(UserCreationForm):
    bio = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 100}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'username', 'email', 'bio', 'avatar']


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ('username', 'password')
        help_texts = {
            'username': None,
            'password': None,
        }


class CustomUserEditForm(UserChangeForm):
    bio = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 100}))

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'avatar',
        ]


class UserPasswordResetForm(PasswordResetForm):

    class Meta:
        model = Profile
        fields = ('email',)


class UserPasswordResetConfirmForm(SetPasswordForm):

    class Meta:
        model = Profile
        fields = ('password',)
