from django import forms
from .models import Factuur

class FactuurForm(forms.ModelForm):
    class Meta:
        model = Factuur
        fields = [
            'factuurnummer',
            'datum',
            'factuur_type',
            'bedrag_excl_btw',
            'btw_percentage',
            'totaal_bedrag',
            'status',
            'debiteur',
            'crediteur'
        ]
        widgets = {
            'datum': forms.DateInput(attrs={'type': 'date'}),
        }
