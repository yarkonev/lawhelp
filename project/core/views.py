from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Plaintiff, Defendant
from .forms import CaseForm, PlaintiffForm, DefendantForm
from core.make_doc import *


def index(request):
    return render(request, 'core/index.html')


def cases(request):
    cases = Case.objects.all()
    context = {
        'cases': cases,
    }
    return render(request, 'core/cases.html', context)


def case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)
    context = {
        'case': case,
        'plaintiff': case.plaintiff,
        'defendant': case.defendant,
        'court': case.court,
        'number': case.number,
        'overall_charge': case.overall_charge,
        'gp_charge': case.gp_charge,
    }
    return render(request, 'core/case.html', context)


def new_plaintiff(request):
    if request.method != 'POST':
        form = PlaintiffForm()
    else:
        form = PlaintiffForm(data=request.POST)
        if form.is_valid():
            new_plaintiff = form.save(commit=False)
            new_plaintiff.save()
            return redirect('core:cases')

    context = {
        'form': form,
    }

    return render(request, 'core/new_plaintiff.html', context)


def new_defendant(request):
    if request.method != 'POST':
        form = DefendantForm()
    else:
        form = DefendantForm(data=request.POST)
        if form.is_valid():
            new_defendant = form.save(commit=False)
            new_defendant.save()
            return redirect('core:cases')

    context = {
        'form': form,
    }

    return render(request, 'core/new_defendant.html', context)


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


def edit_case(request, case_id):
    case = Case.objects.get(id=case_id)

    if request.method != 'POST':
        form = CaseForm(instance=case)
    else:
        form = CaseForm(instance=case, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:case', case_id=case.id)

    context = {
        'case': case,
        'form': form,
    }

    return render(request, 'core/edit_case.html', context)


def plaintiff_detail(request, plaintiff_id):
    plaintiff = get_object_or_404(Plaintiff, id=plaintiff_id)
    context = {
        'plaintiff': plaintiff,
    }
    return render(request, 'core/plaintiff_detail.html', context)


def defendant_detail(request, defendant_id):
    defendant = get_object_or_404(Defendant, id=defendant_id)
    context = {
        'defendant': defendant,
    }
    return render(request, 'core/defendant_detail.html', context)


def make_petition_view(request, case_id):
    case = Case.objects.get(id=case_id)
    return make_petition(case)
