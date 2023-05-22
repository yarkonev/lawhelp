from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import CaseForm, DefendantForm, PlaintiffForm
from .make_doc import make_petition
from .models import Case, Defendant, Plaintiff
from .services import count_court_fee


def index(request):
    return render(request, 'home/index.html')


@login_required
def home(request):
    return render(request, 'home/home.html')


@login_required
def cases(request):
    """
    View function that retrieves all Case objects from the database and renders
    them using the 'core/cases.html' template.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response object that contains the rendered
    template with the retrieved Case objects.
    """
    cases = Case.objects.all()
    context = {
        'cases': cases,
    }
    return render(request, 'core/cases.html', context)


@login_required
def case(request, case_id):
    """
    Renders the detail view of a legal case identified by its primary key.

    Args:
    - request: the HTTP request object
    - case_id: the primary key of the case object to retrieve

    Returns:
    - an HTTP response with the rendered case template

    Raises:
    - Http404: If the case with the given id does not exist.
    """
    case = get_object_or_404(Case, case_id=case_id)
    context = {
        'case': case,
        'plaintiff': case.plaintiff,
        'defendant': case.defendant,
        'court': case.court,
        'appeals_court': case.appeals_court,
        'number': case.number,
        'claim_price': case.claim_price,
        'gp_charge': case.gp_charge,
    }
    return render(request, 'core/case.html', context)


@login_required
def plaintiffs(request):
    """
    View function that retrieves all Case objects from the database and renders
    them using the 'core/cases.html' template.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response object that contains the rendered
    template with the retrieved Case objects.
    """
    plaintiffs = Plaintiff.objects.all()
    context = {
        'plaintiffs': plaintiffs,
    }
    return render(request, 'core/plaintiffs.html', context)


@login_required
def new_plaintiff(request):
    if request.method != 'POST':
        form = PlaintiffForm()
    else:
        form = PlaintiffForm(data=request.POST)
        if form.is_valid():
            new_plaintiff = form.save(commit=False)
            new_plaintiff.save()
            return redirect('core:plaintiffs')

    context = {
        'form': form,
    }

    return render(request, 'core/new_plaintiff.html', context)


@login_required
def defendants(request):
    defendants = Defendant.objects.all()
    context = {
        'defendants': defendants,
    }
    return render(request, 'core/defendants.html', context)


@login_required
def new_defendant(request):
    if request.method != 'POST':
        form = DefendantForm()
    else:
        form = DefendantForm(data=request.POST)
        if form.is_valid():
            new_defendant = form.save(commit=False)
            new_defendant.save()
            return redirect('core:defendants')

    context = {
        'form': form,
    }

    return render(request, 'core/new_defendant.html', context)


@login_required
def new_case(request):
    """
    Create a new case from a POST request or display an empty case form.
    If the request is not a POST request, display
    an empty case form.
    If the request is a POST request, validate the form data and
    create a new case.
    If the new case has no GP charge, calculate it based on the claim price.
    Redirect to the list of cases after creating the new case.

    Args:
    - request (HttpRequest): The HTTP request containing the form data.

    Returns:
    - HttpResponse: The HTTP response containing the rendered template.
    """
    if request.method != 'POST':
        form = CaseForm()
    else:
        form = CaseForm(data=request.POST)
        if form.is_valid():
            new_case = form.save(commit=False)
            if not new_case.gp_charge:
                new_case.gp_charge = count_court_fee(new_case.claim_price)
            new_case.save()
            return redirect('core:cases')

    context = {
        'form': form,
    }
    return render(request, 'core/new_case.html', context)


@login_required
def edit_case(request, case_id):
    """
    Renders a form to edit a Case object identified by `case_id`, or saves the
    changes to the object if the form is submitted and valid.

    Args:
    - request (HttpRequest): The HTTP request object.
    - case_id (int): The ID of the Case object to edit.

    Returns:
    - HttpResponse: A response containing the form to edit the Case object,
    or a redirect to the Case object's detail view if the changes were saved
    successfully.
    """
    case = Case.objects.get(case_id=case_id)

    if request.method != 'POST':
        form = CaseForm(instance=case)
    else:
        form = CaseForm(instance=case, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:case', case_id=case_id)

    context = {
        'case': case,
        'form': form,
    }

    return render(request, 'core/edit_case.html', context)


@login_required
def plaintiff_detail(request, firm_id):
    plaintiff = get_object_or_404(Plaintiff, firm_id=firm_id)
    context = {
        'plaintiff': plaintiff,
    }
    return render(request, 'core/plaintiff_detail.html', context)


@login_required
def defendant_detail(request, defendant_id):
    """
    Render the detail page for the defendant with the given ID.

    Args:
    - request (HttpRequest): The HTTP request.
    - defendant_id (int): The ID of the defendant to display.

    Returns:
    - HttpResponse: The HTTP response containing the rendered page.

    Raises:
    - Http404: If no defendant exists with the given ID.
    """
    defendant = get_object_or_404(Defendant, firm_id=defendant_id)
    context = {
        'defendant': defendant,
    }
    return render(request, 'core/defendant_detail.html', context)


@login_required
def make_petition_view(request, case_id):
    """
    View function that generates a petition for a given case.

    Args:
    - request (HttpRequest): The request object.
    - case_id (int): The ID of the case for which to generate the petition.

    Returns:
    - HttpResponse: A response containing the generated petition as docx file.
    """
    case = Case.objects.get(case_id=case_id)
    return make_petition(case)
