from django import forms
from .models import NZACode, Werkfase

class NZACodeForm(forms.ModelForm):
    class Meta:
        model = NZACode
        fields = ['code', 'techniekkosten', 'honorarium', 'beschrijving']
        widgets = {
            'beschrijving': forms.Textarea(attrs={'rows': 3}),
        }

class WerkfaseForm(forms.ModelForm):
    class Meta:
        model = Werkfase
        fields = ['volgorde', 'duur']
        widgets = {
            'duur': forms.TextInput(attrs={'placeholder': 'hh:mm:ss'}),
        }
