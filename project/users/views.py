from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('core:home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('core:index')


@login_required
def profile(request):
    return render(request, 'users/profile.html')
