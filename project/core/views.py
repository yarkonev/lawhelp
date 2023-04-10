from django.shortcuts import render
from .models import Case


def index(request):
    return render(request, 'index.html')

def cases(request):
    cases = Case.objects.all()
    context = {
        'cases': cases,
    }
    return render(request, 'cases.html', context)
