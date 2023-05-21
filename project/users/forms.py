from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput)