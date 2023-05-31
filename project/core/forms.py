from django import forms

from .models import Case, Defendant, Plaintiff


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'number', 'status', 'court_level', 'court',
            'appeals_court', 'cassation_court', 'card',
            'plaintiff', 'defendant', 'claim_price', 'gp_charge'
        ]
        labels = {
            'number': 'Номер дела',
            'status': 'Статус дела',
            'court_level': 'Инстанция',
            'court': 'Суд первой инстанции',
            'appeals_court': 'Апелляция',
            'cassation_court': 'Кассация',
            'card': 'Карточка дела',
            'plaintiff': 'Истец',
            'defendant': 'Ответчик',
            'claim_price': 'Цена иска',
            'gp_charge': 'Госпошлина',
        }


class PlaintiffForm(forms.ModelForm):
    class Meta:
        model = Plaintiff
        fields = ['full_name', 'short_name', 'ogrn', 'inn', 'address']
        labels = {'full_name': 'Полное наименование',
                  'short_name': 'Сокращенное наименование',
                  'ogrn': 'ОГРН',
                  'inn': 'ИНН',
                  'address': 'Адрес',
                  }


class DefendantForm(forms.ModelForm):
    class Meta:
        model = Defendant
        fields = ['full_name', 'short_name', 'ogrn', 'inn', 'address']
        labels = {'full_name': 'Полное наименование',
                  'short_name': 'Сокращенное наименование',
                  'ogrn': 'ОГРН',
                  'inn': 'ИНН',
                  'address': 'Адрес',
                  }


class DocumentForm(forms.Form):
    OPTION_CHOICES = (
        ('objection_to_defendant_response', 'Возражение на отзыв ответчика'),
        ('legal_services_contract', 'Договор на оказание юридических услуг'),
        ('application_for_issuance_of_execution_writ', 'Заявление о выдаче исполнительного листа'),
        ('federal_tax_service_request', 'Запрос в ФНС'),
        ('bank_application', 'Заявление в банк'),
        ('application_for_recovery_of_court_costs', 'Заявление о взыскании судебных расходов'),
        ('application_for_duty_setoff', 'Заявление о зачете госпошлины'),
        ('application_for_motivated_decision', 'Заявление о составлении мотивированного решения'),
        ('application_for_enforcement_of_execution_document', 'Заявление об исполнении исполнительного документа'),
        ('envelopes', 'Конверты'),
        ('settlement_agreement', 'Мировое соглашение'),
        ('third_party_explanations', 'Пояснения третьего лица'),
        ('petition', 'Ходатайство'),
        ('motion_for_return_of_complaint', 'Ходатайство о возвращении искового заявления'),
        ('motion_for_retransmission_of_court_order', 'Ходатайство о повторном направлении определения суда'),
        ('motion_for_absentia_review', 'Ходатайство о рассмотрении в отсутствие стороны'),
        ('motion_for_online_participation', 'Ходатайство об участии онлайн'),
        ('appeal_brief', 'Апелляционная жалоба (краткая)'),
        ('case_explanation', 'Объяснение по делу'),
        ('motion_for_submission_of_evidence', 'Ходатайство о приобщении доказательств')
    )

    documents = forms.MultipleChoiceField(
        label='Создать документы',
        choices=OPTION_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'})