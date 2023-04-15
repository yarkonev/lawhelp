import os
import io
from django.conf import settings
from django.http import HttpResponse
from docxtpl import DocxTemplate


def make_petition(case):

    # Open template document
    document = DocxTemplate(os.path.join(settings.STATICFILES_DIRS[0], 'docx_templates/template_petition.docx'))

    # Update template with data
    context = {
        'case_num': case.number,
        'court_name': case.court.name,
        'court_index': case.court.zip_code,
        'court_address': case.court.address,
        'defendant_name': case.defendant.short_name,
        'defendant_inn': case.defendant.inn,
        'defendant_ogrn': case.defendant.ogrn,
        'defendant_address': case.defendant.address,
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
