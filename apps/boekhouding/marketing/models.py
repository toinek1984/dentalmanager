from django.db import models
from apps.boekhouding.grootboekrekeningen.models import Grootboekrekening  # ⬅ import toegevoegd

STRATEGIE_CHOICES = [
    ('google', 'Google'),
    ('facebook', 'Facebook'),
    ('krant', 'Krant'),
    ('radio', 'Radio'),
    ('viavia', 'Viavia'),
    ('folder', 'Folder'),
    ('sponsoring', 'Sponsoring'),
    ('anders', 'Anders'),
]

class Provincie(models.Model):
    naam = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.naam

class MarketingCampagne(models.Model):
    naam = models.CharField(max_length=200, unique=True)
    startdatum = models.DateField()
    einddatum = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    uitgegeven_bedrag = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    omschrijving = models.TextField(blank=True)
    actief = models.BooleanField(default=True)
    provincie = models.ForeignKey(
        Provincie,
        on_delete=models.CASCADE,
        related_name='campagnes',
        null=True,
        blank=True
    )
    strategie = models.CharField(
        max_length=50,
        choices=STRATEGIE_CHOICES,
        blank=True
    )
    archived = models.BooleanField(default=False)

    # ➕ NIEUW: koppeling naar grootboekrekening
    grootboekrekening = models.ForeignKey(
        Grootboekrekening,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Grootboekrekening"
    )

    def __str__(self):
        provincie_str = f" ({self.provincie})" if self.provincie else ""
        return f"{self.naam}{provincie_str}"
