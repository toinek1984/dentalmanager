from django.db import models
from apps.boekhouding.tarieven.models import NZACode

FACTURERING_CHOICES = (
    ('facturabel', 'Facturabel'),
    ('garantie', 'Garantie'),
)

class Werkbon(models.Model):
    werkbonnummer = models.CharField("Werkbonnummer", max_length=20, unique=True)
    klant = models.CharField("Klant", max_length=100)
    behandelaar = models.CharField("Behandelaar", max_length=100)
    facturabel_garantie = models.CharField("Facturering", max_length=20, choices=FACTURERING_CHOICES)
    # In plaats van honorarium gebruiken we hier verkoopwaarde
    verkoopwaarde = models.DecimalField("Verkoopwaarde", max_digits=10, decimal_places=2, default=0.0)
    inkoopwaarde = models.DecimalField("Inkoopwaarde", max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField("Status", max_length=20)
    aanmaakdatum = models.DateField(auto_now_add=True)
    nza_code = models.ForeignKey(
        'tarieven.NZACode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='werkbon_kunstgebitaanhuis'
    )

    def __str__(self):
        return self.werkbonnummer

    class Meta:
        verbose_name = 'Werkbon'
        verbose_name_plural = 'Werkbonnen'
