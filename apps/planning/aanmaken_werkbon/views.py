import random
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest, JsonResponse

# Let op: controleer of deze importlocaties overeenkomen met jouw project.
# In veel projecten staat het Klant-model in apps/klanten/models.py,
# maar hier gaan we ervan uit dat je het via apps/planning.models importeert.
from apps.planning.models import Werkbon, Klant, Opdrachtgever, generate_werkbonnummer
from apps.boekhouding.tarieven.models import NZACode
from apps.hr.werknemers.models import Werknemer
from apps.planning.forms import WerkbonForm  # Zorg dat je een ModelForm voor Werkbon hebt

# --------------------------------------------------------------------------------------
# AJAX zoekfuncties
# --------------------------------------------------------------------------------------
def search_klant(request):
    """
    Zoekt klanten op basis van de zoekterm in het 'term'-queryparameter.
    Retourneert een JSON-lijst met de gevonden klantgegevens.
    """
    zoekterm = request.GET.get('term', '').strip()
    # We zoeken in het veld 'naam'. Pas dit aan als jouw model andere velden heeft (bv. voornaam, achternaam).
    klanten = Klant.objects.filter(naam__icontains=zoekterm).values(
        'id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email'
    )
    return JsonResponse(list(klanten), safe=False)

def search_opdrachtgever(request):
    """
    Zoekt opdrachtgevers op basis van de zoekterm in het 'term'-queryparameter.
    Retourneert een JSON-lijst met de gevonden opdrachtgevergegevens.
    """
    zoekterm = request.GET.get('term', '').strip()
    opdrachtgevers = Opdrachtgever.objects.filter(naam__icontains=zoekterm).values(
        'id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email'
    )
    return JsonResponse(list(opdrachtgevers), safe=False)

# --------------------------------------------------------------------------------------
# Helperfunctie voor het aanmaken van een klantdossier
# --------------------------------------------------------------------------------------
def create_klantdossier_for_klant(klant):
    """
    Deze functie maakt (of controleert) een klantdossier voor de gegeven klant.
    Pas de implementatie aan op basis van jouw eigen logica en het model van het klantdossier.
    """
    # Voorbeeld: als je KlantDossier in apps/klanten/klantdossier/models.py staat
    from apps.klanten.klantdossier.models import KlantDossier
    dossier, created = KlantDossier.objects.get_or_create(klant=klant)
    if created:
        print(f"Klantdossier aangemaakt voor: {klant.naam}")
    else:
        print(f"Klantdossier bestaat al voor: {klant.naam}")
    return dossier

# --------------------------------------------------------------------------------------
# View voor het aanmaken van een nieuwe werkbon
# --------------------------------------------------------------------------------------
def create_werkbon(request):
    """
    Deze view verwerkt een POST-request om een nieuwe werkbon aan te maken.
    Hij haalt klantgegevens op, maakt (indien nodig) een klant en een klantdossier,
    verwerkt opdrachtgevergegevens en de werkbon-specifieke gegevens, genereert een uniek werkbonnummer,
    en maakt de werkbon aan. Afhankelijk van de actie (opslaan of opslaan en print) wordt er geredirect.
    """
    if request.method == "POST":
        # ----- Klantgegevens ophalen of aanmaken -----
        klant_naam = request.POST.get('klant_naam', '').strip()
        if not klant_naam:
            return HttpResponseBadRequest("Klantnaam is verplicht.")
        klant_adres = request.POST.get('klant_adres', '')
        klant_woonplaats = request.POST.get('klant_woonplaats', '')
        klant_geboortedatum = request.POST.get('klant_geboortedatum') or None
        klant_telefoon = request.POST.get('klant_telefoon', '')
        klant_email = request.POST.get('klant_email', '')
        klant_verzekeringsnummer = request.POST.get('klant_verzekeringsnummer', '')

        # Gebruik get_or_create om een klant te vinden of aan te maken.
        klant, created = Klant.objects.get_or_create(
            naam=klant_naam,
            defaults={
                'adres': klant_adres,
                'woonplaats': klant_woonplaats,
                'geboortedatum': klant_geboortedatum,
                'telefoon': klant_telefoon,
                'email': klant_email,
                'verzekeringsnummer': klant_verzekeringsnummer,
            }
        )

        # Maak een klantdossier aan als de klant nieuw is.
        if created:
            create_klantdossier_for_klant(klant)

        # ----- Opdrachtgevergegevens ophalen of aanmaken -----
        opdrachtgever_naam = request.POST.get('opdrachtgever_naam', '').strip()
        opdrachtgever = None
        if opdrachtgever_naam:
            opdrachtgever = Opdrachtgever.objects.filter(naam__iexact=opdrachtgever_naam).first()
            if not opdrachtgever:
                opdrachtgever = Opdrachtgever.objects.create(
                    naam=opdrachtgever_naam,
                    adres=request.POST.get('opdrachtgever_adres', ''),
                    telefoon=request.POST.get('opdrachtgever_telefoon', ''),
                    email=request.POST.get('opdrachtgever_email', '')
                )

        # ----- Werkbon Specifieke Gegevens -----
        gebitsdatum = request.POST.get('gebitsdatum') or None
        tandkleur = request.POST.get('tandkleur', '')
        aanvang_werkzaamheden = None  # Wordt later ingesteld door de planning
        naaminpersen = (request.POST.get('naaminpersen') == 'on')

        # Haal werknemer-ID's op voor behandelaar en technicus.
        behandelaar_id = request.POST.get('behandelaar', '').strip()
        technicus_id = request.POST.get('technicus', '').strip()
        if not behandelaar_id.isdigit():
            return HttpResponseBadRequest("Ongeldig of ontbrekend behandelaar-ID.")
        if not technicus_id.isdigit():
            return HttpResponseBadRequest("Ongeldig of ontbrekend technicus-ID.")
        try:
            behandelaar = Werknemer.objects.get(id=int(behandelaar_id))
        except Werknemer.DoesNotExist:
            return HttpResponseBadRequest("Behandelaar niet gevonden.")
        try:
            technicus = Werknemer.objects.get(id=int(technicus_id))
        except Werknemer.DoesNotExist:
            return HttpResponseBadRequest("Technicus niet gevonden.")

        if not behandelaar.naam:
            return HttpResponseBadRequest("De geselecteerde behandelaar heeft geen naam.")

        notities = request.POST.get('notities', '')
        facturabel_garantie = request.POST.get('facturabel_garantie', '')

        # ----- Verwerk het NZACode veld -----
        nza_code_pk = request.POST.get('nza_code', '').strip()
        nza_instance = None
        if nza_code_pk.isdigit():
            try:
                nza_instance = NZACode.objects.get(pk=int(nza_code_pk))
            except NZACode.DoesNotExist:
                nza_instance = None

        # ----- Genereer een uniek werkbonnummer -----
        base_werkbonnummer = generate_werkbonnummer()  # Bijvoorbeeld: "A787F98C"
        werkbonnummer = f"{base_werkbonnummer}_{random.randint(1000, 9999)}"

        # ----- Maak de Werkbon aan -----
        werkbon = Werkbon.objects.create(
            klant=klant,
            opdrachtgever=opdrachtgever,
            gebitsdatum=gebitsdatum,
            tandkleur=tandkleur,
            aanvang_werkzaamheden=aanvang_werkzaamheden,
            naaminpersen=naaminpersen,
            # Opmerking: Zorg ervoor dat het veld 'behandelaar' in het Werkbon-model
            # juist gedefinieerd is (als ForeignKey verwacht dan geef je het klantobject mee,
            # als CharField geef je de naam mee). Hier gaan we ervan uit dat het een CharField is.
            behandelaar=behandelaar.naam,
            technicus=technicus.naam,
            notities=notities,
            nza_code=nza_instance,
            facturabel_garantie=facturabel_garantie,
            werkbonnummer=werkbonnummer
        )

        print("Werkbon aangemaakt met barcode:", werkbon.barcode)

        # Redirect afhankelijk van de actie ("print" of "save")
        if request.POST.get('action') == 'print':
            return redirect(reverse('planning:werkbon_print', args=[werkbon.pk]))
        else:
            return redirect(reverse('planning:planboard'))

    # Voor GET-verzoeken: toon het formulier
    nza_codes = NZACode.objects.all()
    werknemers = Werknemer.objects.all()
    context = {
        'nza_codes': nza_codes,
        'werknemers': werknemers,
    }
    return render(request, 'planning/form.html', context)

# --------------------------------------------------------------------------------------
# Edit view voor bestaande werkbonnen
# --------------------------------------------------------------------------------------
def edit_werkbon(request, pk):
    """
    Deze view laadt een bestaande werkbon en laat deze bewerken met een ModelForm.
    """
    werkbon = get_object_or_404(Werkbon, pk=pk)
    if request.method == "POST":
        form = WerkbonForm(request.POST, instance=werkbon)
        if form.is_valid():
            form.save()
            return redirect(reverse('planning:werkbon_overzicht'))
        else:
            # Toon het formulier opnieuw als er fouten zijn
            return render(request, 'planning/edit_werkbon.html', {'form': form, 'werkbon': werkbon})
    else:
        form = WerkbonForm(instance=werkbon)
    return render(request, 'planning/edit_werkbon.html', {'form': form, 'werkbon': werkbon})
