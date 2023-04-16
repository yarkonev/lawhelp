from django.contrib import admin

from .models import Case, Court, Defendant, Plaintiff


admin.site.register(Court)
admin.site.register(Defendant)
admin.site.register(Plaintiff)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'court', 'card',
        'plaintiff', 'defendant',
        'overall_charge', 'gp_charge'
    )
