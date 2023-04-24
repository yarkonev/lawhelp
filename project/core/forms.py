from django import forms

from .models import Case, Defendant, Plaintiff


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['number', 'court', 'appeals_court', 'card', 'plaintiff', 'defendant', 'overall_charge', 'gp_charge']
        labels = {'number': 'Номер дела',
                  'court': 'Суд',
                  'appeals_court': 'Апелляционный суд',
                  'card': 'Карточка дела',
                  'plaintiff': 'Истец',
                  'defendant': 'Ответчик',
                  'overall_charge': 'Цена иска',
                  'gp_charge': 'Госпошлина',
                  }


class PlaintiffForm(forms.ModelForm):
    class Meta:
        model = Plaintiff
        fields = ['full_name', 'short_name', 'ogrn', 'inn', 'address']
        labels = {'full_name': 'Полное наименование',
                  'short_name': 'Краткое наименование',
                  'ogrn': 'ОГРН',
                  'inn': 'ИНН',
                  'address': 'Адрес',
                  }


class DefendantForm(forms.ModelForm):
    class Meta:
        model = Defendant
        fields = ['full_name', 'short_name', 'ogrn', 'inn', 'address']
        labels = {'full_name': 'Полное наименование',
                  'short_name': 'Краткое наименование',
                  'ogrn': 'ОГРН',
                  'inn': 'ИНН',
                  'address': 'Адрес',
                  }
