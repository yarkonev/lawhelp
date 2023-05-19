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
        'overall_charge': case.overall_charge,
        'gp_charge': case.gp_charge,
    }
    return render(request, 'core/case.html', context)


@login_required
def new_plaintiff(request):
    """
    View function for creating a new plaintiff.
    If the request method is GET, render the plaintiff form.
    If the request method is POST, validate the form data and
    save a new plaintiff.
    If the form is invalid, render the plaintiff form with errors.
    If the plaintiff is successfully saved, redirect to the 'cases' page.

    Args:
    - request: the HTTP request object

    Returns:
    - If the request method is GET, a rendered 'new_plaintiff'
    template with the plaintiff form.
    - If the request method is POST and the form is invalid, a rendered
    'new_plaintiff' template with the plaintiff form and errors.
    - If the request method is POST and the plaintiff is successfully
    saved, a redirect to the 'cases' page.
    """
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


@login_required
def new_defendant(request):
    """
    This function creates a new defendant object
    with the data provided by the user through a POST request.
    If the request method is GET, it returns a new DefendantForm object.
    If the request method is POST and the form is valid,
    the new defendant object is saved and the user is redirected
    to the 'core:cases' URL.
    If the form is invalid, it renders the 'core/new_defendant.html'
    template with the invalid form and returns the resulting HTML.

    Args:
    - request (HttpRequest): The HTTP request containing the form data.

    Returns:
    - HttpResponse: The HTTP response containing the rendered template.
    """
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


@login_required
def new_case(request):
    """
    Create a new case from a POST request or display an empty case form.
    If the request is not a POST request, display
    an empty case form.
    If the request is a POST request, validate the form data and
    create a new case.
    If the new case has no GP charge, calculate it based on the overall charge.
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
                new_case.gp_charge = count_court_fee(new_case.overall_charge)
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
def plaintiff_detail(request, plaintiff_id):
    """
    Render a defendant's detail page based on their id.

    Args:
    - request: A Django HttpRequest object.
    - defendant_id: An integer representing the id of the defendant.

    Returns:
    - A rendered HttpResponse object with the context containing the defendant
    information.

    Raises:
    - Http404: If no defendant exists with the given ID.
    """
    plaintiff = get_object_or_404(Plaintiff, firm_id=plaintiff_id)
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
