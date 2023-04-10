from django.shortcuts import render
from .models import Case
from .forms import CaseForm


def index(request):
    return render(request, 'index.html')


def cases(request):
    cases = Case.objects.all()
    context = {
        'cases': cases,
    }
    return render(request, 'core/cases.html', context)


def new_case(request):
    if request.method != 'POST':
        form = CaseForm()
    else:
        form = CaseForm(data=request.POST)
        if form.is_valid():
            new_case = form.save(commit=False)
            new_case.save()
            return redirect('core:cases')
    
    context = {
        'form': form,
    }
    return render(request, 'core/new_case.html', context)