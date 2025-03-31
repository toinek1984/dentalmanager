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


# Houd alleen deze uitgebreide definitie van KlantDossier; verwijder de kortere versie!
class KlantDossier(models.Model):
    klantnummer = models.AutoField(primary_key=True)
    voornaam = models.CharField(max_length=100)
    achternaam = models.CharField(max_length=100)
    geboortedatum = models.DateField(blank=True, null=True)
    straat = models.CharField(max_length=200)
    huisnummer = models.CharField(max_length=10)
    postcode = models.CharField(max_length=10)
    woonplaats = models.CharField(max_length=100)
    telefoonnummer = models.CharField(max_length=20)
    emailadres = models.EmailField()
    zorginstelling = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Indien van toepassing"
    )
    onder_bewind = models.BooleanField(
        default=False,
        help_text="Is de klant onder bewind?"
    )
    bewindvoerder_naam = models.CharField(max_length=100, blank=True, null=True)
    bewindvoerder_adres = models.CharField(max_length=200, blank=True, null=True)
    bewindvoerder_telefoon = models.CharField(max_length=20, blank=True, null=True)
    bewindvoerder_email = models.EmailField(blank=True, null=True)
    verzekeringsnummer = models.CharField(max_length=100)
    factuur_geschiedenis = models.JSONField(blank=True, null=True)
    werkbon_geschiedenis = models.JSONField(blank=True, null=True)
    extra_fields = models.JSONField(blank=True, null=True)
    is_overleden = models.BooleanField(
        default=False,
        help_text="Markeer dossier als afgesloten bij overlijden"
    )
    overlijdensdatum = models.DateField(
        blank=True,
        null=True,
        help_text="Datum van overlijden, indien van toepassing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.voornaam} {self.achternaam} ({self.klantnummer})"


class KlantNotitie(models.Model):
    dossier = models.ForeignKey(KlantDossier, on_delete=models.CASCADE, related_name='notities')
    tekst = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notitie voor dossier {self.dossier.klantnummer} op {self.created_at:%d-%m-%Y}"
