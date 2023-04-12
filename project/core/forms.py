from django import forms
from .models import Case, Plaintiff, Defendant


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['number', 'court', 'card', 'plaintiff', 'defendant']
        labels = {'number': 'Номер дела',
                  'court': 'Суд',
                  'card': 'Карточка дела',
                  'plaintiff': 'Истец',
                  'defendant': 'Ответчик',
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