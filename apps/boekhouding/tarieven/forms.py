from django import forms
from datetime import timedelta
from .models import NZACode, Werkfase

class NZACodeForm(forms.ModelForm):
    class Meta:
        model = NZACode
        fields = ['code', 'techniekkosten', 'honorarium', 'beschrijving']
        widgets = {
            'beschrijving': forms.Textarea(attrs={'rows': 3}),
        }

class WerkfaseForm(forms.ModelForm):
    # Voeg twee extra velden toe voor uren en minuten
    uren = forms.ChoiceField(
        choices=[(i, i) for i in range(0, 5)],  # 0 tot 4 uur
        label="Uren"
    )
    minuten = forms.ChoiceField(
        choices=[(15, "15"), (30, "30"), (45, "45")],
        label="Minuten"
    )
    naam = forms.CharField(max_length=100, label="Fase Naam", required=False)
    
    class Meta:
        model = Werkfase
        # We verwerken de duur via de extra velden, dus we nemen 'volgorde' en 'naam'
        fields = ['volgorde', 'naam']

    def clean(self):
        cleaned_data = super().clean()
        uren = int(cleaned_data.get('uren', 0))
        minuten = int(cleaned_data.get('minuten', 0))
        cleaned_data['duur'] = timedelta(hours=uren, minutes=minuten)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.duur = self.cleaned_data['duur']
        if commit:
            instance.save()
        return instance
