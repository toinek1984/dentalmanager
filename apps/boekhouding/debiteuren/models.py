from django.db import models
from apps.boekhouding.grootboekrekeningen.models import Grootboekrekening

class Debiteur(models.Model):
    naam = models.CharField(max_length=200)
    omschrijving = models.TextField(blank=True)
    adres = models.CharField(max_length=300, blank=True)
    telefoonnummer = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    iban = models.CharField(max_length=34, blank=True, help_text="IBAN")
    bic = models.CharField(max_length=11, blank=True, help_text="BIC")
    betaalvoorwaarden = models.CharField(max_length=200, blank=True)
    grootboekrekening = models.ForeignKey(
        Grootboekrekening,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Grootboekrekening"
    )
    aangemaakt_op = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.naam
