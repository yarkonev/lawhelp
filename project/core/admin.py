from django.contrib import admin

from .models import Case, ArbitrCourt, ArbitrAppealsCourt, Defendant, Plaintiff


admin.site.register(Plaintiff)
admin.site.register(Defendant)
admin.site.register(ArbitrCourt)
admin.site.register(ArbitrAppealsCourt)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'court', 'appeals_court', 'card',
        'plaintiff', 'defendant',
        'claim_price', 'gp_charge'
    )
    
