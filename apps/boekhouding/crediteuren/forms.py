from django import forms
from .models import Crediteur

class CrediteurForm(forms.ModelForm):
    class Meta:
        model = Crediteur
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
