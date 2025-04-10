# apps/boekhouding/grootboekrekeningen/models.py
from django.db import models

class Grootboekrekening(models.Model):
    code = models.CharField(max_length=20, verbose_name="Rekeningcode")
    naam = models.CharField(max_length=100, verbose_name="Naam van de rekening")
    omschrijving = models.TextField(blank=True, verbose_name="Omschrijving")

    def __str__(self):
        return f"{self.code} - {self.naam}"

    class Meta:
        verbose_name = "Grootboekrekening"
        verbose_name_plural = "Grootboekrekeningen"
