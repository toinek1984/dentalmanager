from django import forms
from .models import Werknemer

class WerknemerForm(forms.ModelForm):
    class Meta:
        model = Werknemer
        fields = ['voornaam', 'achternaam', 'geboortedatum', 'functie', 'uurloon', 'loonrekening', 'actief']
        widgets = {
            'geboortedatum': forms.DateInput(attrs={'type': 'date'}),
        }
