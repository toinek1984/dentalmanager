import uuid
from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from apps.boekhouding.marketing.models import MarketingCampagne
from apps.boekhouding.tarieven.models import NZACode

# Hulpfuncties
def generate_werkbonnummer():
    """
    Genereer een uniek werkbonnummer (bv. de eerste 8 karakters van een UUID).
    """
    return str(uuid.uuid4())[:8].upper()

def generate_barcode():
    """
    Genereer een barcode voorafgegaan door 'BC'.
    """
    return "BC" + str(uuid.uuid4())[:10].upper()

# --------------------------
# Model voor Klantgegevens
# --------------------------
class Klant(models.Model):
    naam = models.CharField("Naam", max_length=100)
    adres = models.CharField("Adres", max_length=200, blank=True)
    woonplaats = models.CharField("Woonplaats", max_length=100, blank=True)
    geboortedatum = models.DateField("Geboortedatum", null=True, blank=True)
    telefoon = models.CharField("Telefoonnummer", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    verzekeringsnummer = models.CharField("Verzekeringsnummer", max_length=50, blank=True)
    mantelzorger = models.BooleanField("Heeft mantelzorger?", default=False)
    mantelzorger_naam = models.CharField("Mantelzorger Naam", max_length=100, blank=True)
    mantelzorger_telefoon = models.CharField("Mantelzorger Telefoon", max_length=20, blank=True)
    mantelzorger_geboortedatum = models.DateField("Mantelzorger Geboortedatum", null=True, blank=True)
    onder_bewind = models.BooleanField("Onder bewind?", default=False)
    HERKOMST_CHOICES = [
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('krant', 'Krant'),
        ('radio', 'Radio'),
        ('viavia', 'Viavia'),
        ('folder', 'Folder'),
        ('sponsoring', 'Sponsoring'),
        ('anders', 'Anders'),
    ]
    herkomst = models.CharField("Hoe is de klant bij ons gekomen?", max_length=20, choices=HERKOMST_CHOICES, blank=True)

    def __str__(self):
        return self.naam

# -------------------------------
# Model voor Opdrachtgevergegevens
# -------------------------------
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

# --------------------------
# Keuzelijsten voor Werkbon
# --------------------------
TANDKLEUR_CHOICES = [
    ('a1', 'A1'),
    ('a2', 'A2'),
    ('a3', 'A3'),
    ('a3,5', 'A3,5'),
    ('c1', 'C1'),
    ('c2', 'C2'),
]

BEHANDELAAR_CHOICES = [
    ('Jellie', 'Jellie'),
    ('Romy', 'Romy'),
    ('Sabrina', 'Sabrina'),
    ('Ellen', 'Ellen'),
    ('Usman', 'Usman'),
]

TECHNICI_CHOICES = [
    ('Job', 'Job'),
    ('Myrthe', 'Myrthe'),
    ('Jellie', 'Jellie'),
    ('Sabrina', 'Sabrina'),
    ('Romy', 'Romy'),
    ('Ellen', 'Ellen'),
    ('Usman', 'Usman'),
]

FACTURABEL_GARANTIE_CHOICES = [
    ('facturabel', 'Facturabel'),
    ('garantie', 'Garantie'),
]

# --------------------------
# Werkbon Model
# --------------------------
class Werkbon(models.Model):
    werkbonnummer = models.CharField("Werkbonnummer", max_length=20, unique=True, blank=True)
    barcode = models.CharField("Barcode", max_length=100, unique=True, blank=True)
    
    # Koppelingen
    klant = models.ForeignKey(Klant, on_delete=models.SET_NULL, null=True, blank=True, related_name='werkbonnen')
    opdrachtgever = models.ForeignKey(Opdrachtgever, on_delete=models.SET_NULL, null=True, blank=True, related_name='werkbonnen')
    
    # Specifieke werkbongegevens
    gebitsdatum = models.DateField("Gebitsdatum", null=True, blank=True)
    tandkleur = models.CharField("Tandkleur", max_length=10, choices=TANDKLEUR_CHOICES, blank=True)
    aanmaakdatum = models.DateField("Aanmaakdatum", auto_now_add=True)
    aanvang_werkzaamheden = models.DateTimeField("Aanvang werkzaamheden", null=True, blank=True)
    naaminpersen = models.BooleanField("Naaminpersen?", default=False)
    behandelaar = models.CharField("Behandelaar", max_length=100, choices=BEHANDELAAR_CHOICES, blank=True)
    technicus = models.CharField("Technicus", max_length=100, choices=TECHNICI_CHOICES, blank=True)
    notities = models.TextField("Notities", blank=True)
    
    # Extra factureringsvelden
    nza_code = models.ForeignKey(
        NZACode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="NZA Code"
    )
    facturabel_garantie = models.CharField("Facturabel of Garantie", max_length=20, choices=FACTURABEL_GARANTIE_CHOICES, blank=True)
    
    # Financiële velden
    verkoopwaarde = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    inkoopwaarde = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    marketing_optie = models.ForeignKey(MarketingCampagne, on_delete=models.SET_NULL, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_behandeling', 'In behandeling'),
        ('gesloten', 'Gesloten'),
    ]
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='open')
    
    def save(self, *args, **kwargs):
        if not self.werkbonnummer:
            self.werkbonnummer = generate_werkbonnummer()
        if not self.barcode:
            self.barcode = generate_barcode()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Werkbon {self.werkbonnummer}"

# --------------------------
# Tijdregistratie Model
# --------------------------
class WerkUurLog(models.Model):
    werkbon = models.ForeignKey(Werkbon, on_delete=models.CASCADE, related_name='uur_logs')
    werknemer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_tijd = models.DateTimeField("Start Tijd")
    eind_tijd = models.DateTimeField("Eind Tijd", null=True, blank=True)
    
    def __str__(self):
        return f"Uurlog voor {self.werkbon.werkbonnummer} door {self.werknemer}"
