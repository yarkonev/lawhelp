from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, LoginForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:cases')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """
        Validates a form and logs in the user if it exists in the database.
        """
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'users/login.html'
