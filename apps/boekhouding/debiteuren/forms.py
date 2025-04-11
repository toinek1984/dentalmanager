from django import forms
from .models import Debiteur

class DebiteurForm(forms.ModelForm):
    class Meta:
        model = Debiteur
        fields = [
            'naam',
            'omschrijving',
            'adres',
            'telefoonnummer',
            'email',
            'iban',
            'bic',
            'betaalvoorwaarden',
            'grootboekrekening'
        ]
