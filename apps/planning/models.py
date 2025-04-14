import uuid
import os
from datetime import date, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from apps.boekhouding.marketing.models import MarketingCampagne
from apps.boekhouding.tarieven.models import NZACode
from apps.klanten.models import Klant 

# Hulpfuncties
def generate_werkbonnummer():
    """
    Genereer een uniek werkbonnummer (bijv. de eerste 8 karakters van een UUID).
    """
    return str(uuid.uuid4())[:8].upper()

def generate_barcode():
    """
    Genereer een barcode voorafgegaan door 'BC'.
    """
    return "BC" + str(uuid.uuid4())[:10].upper()

def generate_barcode_image(code_value):
    import os
    import barcode
    from barcode.writer import ImageWriter
    Code128 = barcode.get_barcode_class('code128')
    # Writer-opties aangepast voor A6-papier: kleinere modules en geen tekst
    writer_options = {
        'module_width': 0.15,   # nog kleiner dan 0.2
        'module_height': 10.0,  # lager voor een kortere barcode
        'quiet_zone': 1,        # minimaliseer de witruimte
        'write_text': False,    # geen tekst onder de barcode
    }
    barcode_instance = Code128(code_value, writer=ImageWriter())
    filename = f"barcode_{code_value}"
    folder = os.path.join(settings.MEDIA_ROOT, 'barcodes')
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    saved_path = barcode_instance.save(filepath, options=writer_options)
    rel_path = os.path.relpath(saved_path, settings.MEDIA_ROOT)
    return rel_path

# --------------------------
# Model voor Klantgegevens (voor zover nodig in planning)
# --------------------------
class Klant(models.Model):
    naam = models.CharField("Naam", max_length=100)
    achternaam = models.CharField("Naam", max_length=100)
    adres = models.CharField("Adres", max_length=200, blank=True)
    woonplaats = models.CharField("Woonplaats", max_length=100, blank=True)
    geboortedatum = models.DateField("Geboortedatum", null=True, blank=True)
    telefoon = models.CharField("Telefoonnummer", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    verzekeringsnummer = models.CharField("Verzekeringsnummer", max_length=50, blank=True)
    # Overige velden...

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
    werkbonnummer = models.CharField(
        "Werkbonnummer", 
        max_length=20, 
        unique=True, 
        blank=True,
        help_text="Uniek nummer dat de werkbon identificeert."
    )
    barcode = models.CharField(
        "Barcode", 
        max_length=100, 
        unique=True, 
        blank=True,
        help_text="Barcode voor automatische identificatie."
    )
    barcode_image = models.ImageField(
        upload_to='barcodes/', 
        blank=True, 
        null=True,
        help_text="Afbeelding van de gegenereerde barcode."
    )
    
    # Koppeling naar een Klant.
    # Met on_delete=SET_NULL blijven werkbonnen bewaard als de klant verwijderd wordt.
    # Het verbose_name maakt het label in de admin en formulieren overzichtelijk.
    klant = models.ForeignKey(
        Klant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='werkbonnen',
        verbose_name="Klant"
        
    )    
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
        if not self.barcode_image:
            self.barcode_image = generate_barcode_image(self.barcode)
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
