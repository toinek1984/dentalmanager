# apps/boekhouding/laboratorium/models.py

from django.db import models
from apps.boekhouding.tarieven.models import NZACode

# Model voor Werkbonnen
class Werkbon(models.Model):
    werkbonnummer = models.CharField("Werkbonnummer", max_length=20, unique=True)
    klant = models.CharField("Klant", max_length=100)
    technicus = models.CharField("Technicus", max_length=100)
    facturabel_garantie = models.CharField("Facturabel of Garantie", max_length=20)
    omzet = models.DecimalField("Omzet", max_digits=10, decimal_places=2, default=0.0)

    # Relatie naar de NZA-code
    nza_code = models.ForeignKey(
        'tarieven.NZACode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='werkbon_laboratorium'
    )

    def __str__(self):
        return self.werkbonnummer

    class Meta:
        verbose_name = 'Werkbon'
        verbose_name_plural = 'Werkbonnen'
