from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest, JsonResponse
from apps.planning.models import Werkbon, Klant, Opdrachtgever
from apps.boekhouding.tarieven.models import NZACode
from apps.hr.werknemers.models import Werknemer

def search_klant(request):
    zoekterm = request.GET.get('term', '').strip()
    klanten = Klant.objects.filter(naam__icontains=zoekterm).values(
        'id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email'
    )
    return JsonResponse(list(klanten), safe=False)

def search_opdrachtgever(request):
    zoekterm = request.GET.get('term', '').strip()
    opdrachtgevers = Opdrachtgever.objects.filter(naam__icontains=zoekterm).values(
        'id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email'
    )
    return JsonResponse(list(opdrachtgevers), safe=False)

def create_klantdossier_for_klant(klant):
    """
    Helperfunctie: Maak een klantdossier aan voor de gegeven klant.
    Voeg hier jouw logica toe (bijvoorbeeld een record in het KlantDossier-model).
    """
    print(f"Klantdossier wordt aangemaakt voor: {klant.naam}")
    # Voorbeeld: KlantDossier.objects.create(klant=klant, ...)

def create_werkbon(request):
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

        klant, _ = Klant.objects.get_or_create(
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
        # Omdat de werkbon in de container blijft (ongepland) geven we geen startdatum door.
        gebitsdatum = request.POST.get('gebitsdatum') or None
        tandkleur = request.POST.get('tandkleur', '')
        aanvang_werkzaamheden = None
        naaminpersen = (request.POST.get('naaminpersen') == 'on')

        # Haal de werknemer-ID’s op en controleer of ze numeriek zijn
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

        # ----- Maak de Werkbon aan -----
        werkbon = Werkbon.objects.create(
            klant=klant,
            opdrachtgever=opdrachtgever,
            gebitsdatum=gebitsdatum,
            tandkleur=tandkleur,
            aanvang_werkzaamheden=aanvang_werkzaamheden,
            naaminpersen=naaminpersen,
            behandelaar=behandelaar,
            technicus=technicus,
            notities=notities,
            nza_code=nza_instance,
            facturabel_garantie=facturabel_garantie,
        )

        # Indien aangevinkt: maak ook een klantdossier aan
        if request.POST.get('create_klantdossier') == 'on':
            create_klantdossier_for_klant(klant)

        # Redirect naar het planboard zodat de werkbon in de container verschijnt
        return redirect(reverse('planning:planboard'))

    # Voor GET-verzoeken: haal alle benodigde data op en toon het formulier
    nza_codes = NZACode.objects.all()
    werknemers = Werknemer.objects.all()
    context = {
        'nza_codes': nza_codes,
        'werknemers': werknemers,
    }
    return render(request, 'planning/form.html', context)
