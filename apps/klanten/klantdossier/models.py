# apps/klanten/klantdossier/models.py
from django.db import models
from apps.klanten.models import Klant  # Zorg dat dit de correcte Klant-definitie is

class KlantDossier(models.Model):
    klant = models.OneToOneField(Klant, on_delete=models.CASCADE, related_name='klantdossier')
    notities = models.TextField(blank=True, null=True)
    # Voeg eventueel andere velden toe

    def __str__(self):
        return f'Dossier voor {self.klant.voornaam} {self.klant.achternaam}'
