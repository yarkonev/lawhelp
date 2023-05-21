from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.forms.widgets import EmailInput
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form that uses email instead of username.
    Added widgets with page style matching.
    """
    email = forms.EmailField(error_messages={
        'unique': 'Аккаунт с такой почтой уже зарегистрирован.'
        },
        widget=EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'}
        )
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'}
        )
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class LoginForm(AuthenticationForm):
    """
    Custom authentication form that uses email instead of username.
    Added widgets with page style matching.
    """
    username = forms.EmailField(
        label=_("Email"),
        widget=EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Email'}
            )
    )
    password = forms.CharField(
        label="Password", strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True,
            'placeholder': 'Password'}
            )
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
