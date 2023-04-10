from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('cases/', views.cases, name='cases'),
    path('case/<uuid:case_id>/', views.case, name='case'),
    path('new_case/', views.new_case, name='new_case'),
]
