from django import forms
from .models import KlantDossier
from .models import KlantNotitie

class KlantDossierForm(forms.ModelForm):
    class Meta:
        model = KlantDossier
        fields = [
            'voornaam', 'achternaam', 'geboortedatum', 'straat', 'huisnummer', 'postcode',
            'woonplaats', 'telefoonnummer', 'emailadres', 'zorginstelling', 'onder_bewind',
            'bewindvoerder_naam', 'bewindvoerder_adres', 'bewindvoerder_telefoon', 'bewindvoerder_email',
            'verzekeringsnummer'
        ]

class KlantNotitieForm(forms.ModelForm):
    class Meta:
        model = KlantNotitie
        fields = ['tekst']
        widgets = {
            'tekst': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Voer hier je notitie in...'}),
        }        