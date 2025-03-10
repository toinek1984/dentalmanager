from django.db import models

# Kiesopties voor de marketingstrategie (indien gewenst)
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
    # Archivering: als de campagne handmatig is gearchiveerd
    archived = models.BooleanField(default=False)

    def __str__(self):
        provincie_str = f" ({self.provincie})" if self.provincie else ""
        return f"{self.naam}{provincie_str}"
