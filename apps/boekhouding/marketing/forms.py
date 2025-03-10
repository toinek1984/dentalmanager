from django import forms
from .models import MarketingCampagne

class MarketingCampagneForm(forms.ModelForm):
    class Meta:
        model = MarketingCampagne
        fields = [
            'naam', 'startdatum', 'einddatum', 'budget',
            'uitgegeven_bedrag', 'omschrijving', 'provincie',
            'strategie', 'actief', 'archived'
        ]
        widgets = {
            'startdatum': forms.DateInput(attrs={'type': 'date'}),
            'einddatum': forms.DateInput(attrs={'type': 'date'}),
        }
