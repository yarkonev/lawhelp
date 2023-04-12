from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('cases/', views.cases, name='cases'),
    path('case/<uuid:case_id>/', views.case, name='case'),
    path('new_plaintiff/', views.new_plaintiff, name='new_plaintiff'),
    path('new_defendant/', views.new_defendant, name='new_defendant'),
    path('new_case/', views.new_case, name='new_case'),
    path('edit_case/<uuid:case_id>/', views.edit_case, name='edit_case'),
    path('create_docx/<uuid:case_id>/', views.create_docx, name='create_docx'),
]
