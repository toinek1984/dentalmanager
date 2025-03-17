from django.db import models

class Werknemer(models.Model):
    naam = models.CharField(max_length=255)
    functie = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefoonnummer = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.naam
