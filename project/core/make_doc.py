import os
import io

from django.conf import settings
from django.http import HttpResponse
from docxtpl import DocxTemplate


def make_petition(case, selected_documents):

    # Getting information about a case
    context = {
        'case_num': case.number,
        'court_name': case.court.name,
        'court_index': case.court.zip_code,
        'court_address': case.court.address,
        'plaintiff_name': case.plaintiff.short_name,
        'plaintiff_inn': case.plaintiff.inn,
        'plaintiff_address': case.plaintiff.address,
        'plaintiff_ogrn': case.plaintiff.ogrn,
        'defendant_name': case.defendant.short_name,
        'defendant_inn': case.defendant.inn,
        'defendant_ogrn': case.defendant.ogrn,
        'defendant_address': case.defendant.address,
    }

    # Open template document
    document = DocxTemplate(os.path.join(
        settings.STATICFILES_DIRS[0],
        'docx_templates/petition.docx')
        )

    # Update template with data
    document.render(context, autoescape=True)

    # Create a file-like buffer to receive .docx data.
    buffer = io.BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Send the document as a response
    response = HttpResponse(buffer.read(),
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=petition.docx'
    return response
