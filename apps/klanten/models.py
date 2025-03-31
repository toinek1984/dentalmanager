# apps/klanten/models.py
from django.db import models

class Klant(models.Model):
    naam = models.CharField(max_length=255)
    adres = models.CharField(max_length=255, blank=True, null=True)
    woonplaats = models.CharField(max_length=255, blank=True, null=True)
    geboortedatum = models.DateField(blank=True, null=True)
    telefoon = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    verzekeringsnummer = models.CharField(max_length=50, blank=True, null=True)
    
    # Nieuwe velden
    mantelzorger = models.BooleanField(default=False)
    mantelzorger_naam = models.CharField(max_length=255, blank=True, null=True)
    mantelzorger_telefoon = models.CharField(max_length=15, blank=True, null=True)
    mantelzorger_geboortedatum = models.DateField(blank=True, null=True)
    onder_bewind = models.BooleanField(default=False)
    herkomst = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.naam

class Opdrachtgever(models.Model):
    naam = models.CharField("Naam", max_length=100)
    adres = models.CharField("Adres", max_length=200, blank=True)
    telefoon = models.CharField("Telefoonnummer", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    kvk = models.CharField("KvK-nummer", max_length=50, blank=True)
    contactpersoon = models.CharField("Contactpersoon", max_length=100, blank=True)
    woonplaats = models.CharField("Woonplaats", max_length=100, blank=True)

    def __str__(self):
        return self.naam
