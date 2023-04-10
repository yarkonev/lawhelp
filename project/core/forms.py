from django import forms
from .models import Case


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
