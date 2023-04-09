from django.contrib import admin
from .models import Court, Plaintiff, Defendant


admin.site.register(Court)
admin.site.register(Defendant)
admin.site.register(Plaintiff)
