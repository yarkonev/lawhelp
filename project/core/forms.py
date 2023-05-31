from django import forms

from .models import Case, Defendant, Plaintiff


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'number', 'legalcase_num', 'status', 'court',
            'appeals_court', 'card',
            'plaintiff', 'defendant', 'claim_price', 'gp_charge'
        ]
        labels = {
            'legalcase_num': 'Внутренний номер дела',
            'number': 'Судебный номер дела',
            'status': 'Статус дела',
            'court': 'Арбитражный суд первой инстанции',
            'appeals_court': 'Арбитражный апелляционный суд',
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
        ('vozrazhenie_na otzyv_otvetchika', 'Возражение на отзыв ответчика'),
        ('dogovor_yuridicheskih_uslug', 'Договор на оказание юридических услуг'),
        ('zayavlenie_o_vydache_ispolnitelnogo_lista', 'Заявление о выдаче исполнительного листа'),
        ('zapros_v_FNS', 'Запрос в ФНС'),
        ('zayavlenie_v_bank', 'Заявление в банк'),
        ('application_for_recovery_of_court_costs', 'Заявление о взыскании судебных расходов'),
        ('zayavlenie_o_zachete_gosposhliny', 'Заявление о зачете госпошлины'),
        ('zayavlenie_o_sostavlenii_motivirovannogo_resheniya', 'Заявление о составлении мотивированного решения'),
        ('application_for_enforcement_of_execution_document', 'Заявление об исполнении исполнительного документа'),
        ('konverty', 'Конверты'),
        ('mirovoe_soglashenie', 'Мировое соглашение'),
        ('third_party_explanations', 'Пояснения третьего лица'),
        ('hodatajstvo', 'Ходатайство'),
        ('hodatajstvo_o_vozvrashenii_iskovogo_zayavleniya', 'Ходатайство о возвращении искового заявления'),
        ('hodatajstvo_o_povtornom_napravlenii_opredeleniya_suda', 'Ходатайство о повторном направлении определения суда'),
        ('hodatajstvo_o_rassmotrenii_v_otsutstvie_storony', 'Ходатайство о рассмотрении в отсутствие стороны'),
        ('hodatajstvo_ob_uchastii_onlajn', 'Ходатайство об участии онлайн'),
        ('apellyacionnaya_zhaloba_(kratkaya)', 'Апелляционная жалоба (краткая)'),
        ('obyasnenie_po_delu', 'Объяснение по делу'),
        ('hodatajstvo_o_priobshenii_dokazatelstv', 'Ходатайство о приобщении доказательств')
    )

    documents = forms.MultipleChoiceField(
        label='Создать документы',
        choices=OPTION_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'})