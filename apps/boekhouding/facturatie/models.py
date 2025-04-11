from django.db import models

class Factuur(models.Model):
    FACTUUR_TYPE_CHOICES = (
        ('verkoop', 'Verkoopfactuur'),
        ('inkoop', 'Inkoopfactuur'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('betaald', 'Betaald'),
        ('vervallen', 'Vervallen'),
    )

    factuurnummer = models.CharField(max_length=100, unique=True)
    datum = models.DateField()
    factuur_type = models.CharField(max_length=10, choices=FACTUUR_TYPE_CHOICES)
    bedrag_excl_btw = models.DecimalField(max_digits=10, decimal_places=2)
    btw_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    totaal_bedrag = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    # Correcte koppeling: gebruik enkel het app_label en het modelnaam
    debiteur = models.ForeignKey(
        'debiteuren.Debiteur',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    crediteur = models.ForeignKey(
        'crediteuren.Crediteur',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    def __str__(self):
        return self.factuurnummer
