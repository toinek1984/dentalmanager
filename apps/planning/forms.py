# apps/planning/forms.py

from django import forms
from .models import Werkbon
from apps.boekhouding.tarieven.models import NZACode

class WerkbonForm(forms.ModelForm):
    # Hier overschrijven we het veld zodat het als een ModelChoiceField wordt weergegeven.
    nza_code = forms.ModelChoiceField(
        queryset=NZACode.objects.all(),
        required=False,
        label="NZA Code",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Werkbon
        fields = [
            'klant',
            'opdrachtgever',
            'gebitsdatum',
            'tandkleur',
            'aanvang_werkzaamheden',
            'naaminpersen',
            'behandelaar',
            'technicus',
            'notities',
            'nza_code',
            'facturabel_garantie',
            # Voeg eventueel andere velden toe die je wilt laten zien
        ]
        widgets = {
            'gebitsdatum': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aanvang_werkzaamheden': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Voeg meer widget-aanpassingen toe indien nodig
        }
