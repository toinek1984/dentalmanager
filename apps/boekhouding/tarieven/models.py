from django.db import models

class NZACode(models.Model):
    code = models.CharField("NZA Code", max_length=20, unique=True)
    techniekkosten = models.DecimalField("Techniekkosten", max_digits=10, decimal_places=2)
    honorarium = models.DecimalField("Honorarium", max_digits=10, decimal_places=2)
    beschrijving = models.CharField("Beschrijving", max_length=60, blank=True)

    def __str__(self):
        return f"{self.code} - {self.beschrijving}"
        
class Werkfase(models.Model):
    nza_code = models.ForeignKey(
        NZACode,
        on_delete=models.CASCADE,
        related_name='werkfases'
    )
    volgorde = models.PositiveIntegerField("Fase Volgorde", default=1)
    duur = models.DurationField("Tijdsduur", null=True, blank=True)

    def __str__(self):
        return f"Fase {self.volgorde}: {self.duur}"
