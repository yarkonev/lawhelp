from django.urls import path

from .views import RegisterView, CustomLoginView, CustomLogoutView


app_name = 'users'
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
