from django.contrib import admin

from .models import Case, Court, AppealsCourt, Defendant, Plaintiff


admin.site.register(Plaintiff)
admin.site.register(Defendant)
admin.site.register(Court)
admin.site.register(AppealsCourt)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'court', 'appeals_court', 'card',
        'plaintiff', 'defendant',
        'overall_charge', 'gp_charge'
    )
