from django import forms
from .models import Case


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'court', 'plaintiff', 'defendant']