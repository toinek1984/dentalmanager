from django.db import models

class Werknemer(models.Model):
    naam = models.CharField(max_length=255)
    functie = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefoonnummer = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        app_label = 'hr'  # ✅ Dit helpt Django de app te herkennen

    def __str__(self):
        return self.naam