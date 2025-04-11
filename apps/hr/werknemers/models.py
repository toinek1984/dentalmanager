from django.db import models
from apps.boekhouding.grootboekrekeningen.models import Grootboekrekening

class Werknemer(models.Model):
    voornaam = models.CharField(max_length=100)
    achternaam = models.CharField(max_length=100)
    geboortedatum = models.DateField()
    functie = models.CharField(max_length=100, blank=True)
    uurloon = models.DecimalField(max_digits=6, decimal_places=2, help_text="Bruto uurloon in euro’s")
    actief = models.BooleanField(default=True)

    # Optioneel: kostenrekening voor loon
    loonrekening = models.ForeignKey(
        Grootboekrekening,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='werknemers',
        verbose_name="Loon Grootboekrekening"
    )

    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"