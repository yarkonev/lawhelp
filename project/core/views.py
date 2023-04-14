from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import Case, Plaintiff
from .forms import CaseForm, PlaintiffForm, DefendantForm
from docxtpl import DocxTemplate
import io
import os


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


def create_docx(request, case_id):
    # Retrieve data from models
    case = Case.objects.get(id=case_id)

    # Open template document
    document = DocxTemplate(os.path.join(settings.STATICFILES_DIRS[0], 'docx_templates/test_template.docx'))

    # Update template with data
    context = {
        'court_name': case.court.name,
        'defendant_name': case.defendant.short_name,
        'defendant_inn': case.defendant.inn,
    }

    document.render(context, autoescape=True)

    # Create a file-like buffer to receive .docx data.
    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Send the document as a response
    response = HttpResponse(buffer.read(),
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=my_document.docx'
    return response
