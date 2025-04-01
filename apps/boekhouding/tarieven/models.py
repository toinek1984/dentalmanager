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
    naam = models.CharField("Fase Naam", max_length=100, blank=True)
    duur = models.DurationField("Tijdsduur", null=True, blank=True)

    def __str__(self):
        # We formatteren de duur als uren:minuten (seconden negeren)
        total_seconds = int(self.duur.total_seconds()) if self.duur else 0
        uren = total_seconds // 3600
        minuten = (total_seconds % 3600) // 60
        return f"Fase {self.volgorde} - {self.naam}: {uren}:{minuten:02d} uur"
