from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import Case
from .forms import CaseForm
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
    }
    return render(request, 'core/case.html', context)


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
