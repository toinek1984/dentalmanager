# apps/boekhouding/tarieven/models.py
from django.db import models


class NZACode(models.Model):
    code = models.CharField("NZA Code", max_length=20, unique=True)
    techniekkosten = models.DecimalField("Techniekkosten", max_digits=10, decimal_places=2)
    honorarium = models.DecimalField("Honorarium", max_digits=10, decimal_places=2)
    beschrijving = models.CharField("Beschrijving", max_length=60, blank=True)

    # Relatie naar Grootboekrekening via string notatie: 'app_label.ModelNaam'
    grootboekrekening = models.ForeignKey(
        'boekhouding_grootboekrekeningen.Grootboekrekening',
        on_delete=models.SET_NULL,     # Rekening mag verwijderd worden, dan blijft deze waarde leeg
        null=True,
        blank=True,
        verbose_name="Grootboekrekening"
    )

    def __str__(self):
        return f"{self.code} - {self.beschrijving}"


class Werkfase(models.Model):
    nza_code = models.ForeignKey(
        NZACode,
        on_delete=models.CASCADE,
        related_name='werkfases'
    )
    volgorde = models.PositiveIntegerField("Fase Volgorde", default=1)
    naam = models.CharField("Fase Naam", max_length=100, blank=True)
    duur = models.DurationField("Tijdsduur", null=True, blank=True)

    def __str__(self):
        if self.duur:
            totaal_seconden = int(self.duur.total_seconds())
            uren = totaal_seconden // 3600
            minuten = (totaal_seconden % 3600) // 60
            return f"Fase {self.volgorde} - {self.naam}: {uren}:{minuten:02d} uur"
        return f"Fase {self.volgorde} - {self.naam}: geen tijd opgegeven"
