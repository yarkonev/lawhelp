from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views import View

from .forms import CustomUserCreationForm, LoginForm


class SignupView(View):
    """
    Handle GET request. Creates a new form for user signup.
    """
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        """
        Handle POST request. If the form is valid, redirects to cases page.
        Otherwise, redirect to signup page.
        """
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:cases')
        return render(request, 'users/signup.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'users/logged_out.html'
