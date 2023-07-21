from django import forms
from .models import CPI

class CPIForm(forms.ModelForm):
    class Meta:
        model = CPI
        fields = ['__all__']