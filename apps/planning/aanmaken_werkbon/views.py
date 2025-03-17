from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from apps.planning.models import Werkbon, Klant, Opdrachtgever
from apps.boekhouding.tarieven.models import NZACode

def search_klant(request):
    """ Zoekt een klant op basis van de naam. Geeft JSON terug. """
    zoekterm = request.GET.get('term', '').strip()
    klanten = Klant.objects.filter(naam__icontains=zoekterm).values('id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email')
    return JsonResponse(list(klanten), safe=False)

def search_opdrachtgever(request):
    """ Zoekt een opdrachtgever op basis van de naam. Geeft JSON terug. """
    zoekterm = request.GET.get('term', '').strip()
    opdrachtgevers = Opdrachtgever.objects.filter(naam__icontains=zoekterm).values('id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email')
    return JsonResponse(list(opdrachtgevers), safe=False)

def create_klantdossier_for_klant(klant):
    """
    Helperfunctie: Maak een klantdossier aan voor de gegeven klant.
    Pas deze functie aan op basis van jouw logica (bijvoorbeeld door een record
    in een KlantDossier-model aan te maken).
    """
    print(f"Klantdossier wordt aangemaakt voor: {klant.naam}")
    # Voorbeeld: KlantDossier.objects.create(klant=klant, ...)

def create_werkbon(request):
    if request.method == "POST":
        # ----- Klantgegevens -----
        klant_naam = request.POST.get('klant_naam')
        klant_adres = request.POST.get('klant_adres', '')
        klant_woonplaats = request.POST.get('klant_woonplaats', '')
        klant_geboortedatum = request.POST.get('klant_geboortedatum') or None
        klant_telefoon = request.POST.get('klant_telefoon', '')
        klant_email = request.POST.get('klant_email', '')
        klant_verzekeringsnummer = request.POST.get('klant_verzekeringsnummer', '')
        
        # Zoek of maak de klant aan
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
        
        # ----- Opdrachtgevergegevens -----
        opdrachtgever_naam = request.POST.get('opdrachtgever_naam')
        opdrachtgever_adres = request.POST.get('opdrachtgever_adres', '')
        opdrachtgever_telefoon = request.POST.get('opdrachtgever_telefoon', '')
        opdrachtgever_email = request.POST.get('opdrachtgever_email', '')
        
        opdrachtgever = None
        if opdrachtgever_naam:
            opdrachtgever, _ = Opdrachtgever.objects.get_or_create(
                naam=opdrachtgever_naam,
                defaults={
                    'adres': opdrachtgever_adres,
                    'telefoon': opdrachtgever_telefoon,
                    'email': opdrachtgever_email,
                }
            )
        
        # ----- Werkbon Specifieke Gegevens -----
        gebitsdatum = request.POST.get('gebitsdatum') or None
        tandkleur = request.POST.get('tandkleur', '')
        aanvang_werkzaamheden = request.POST.get('aanvang_werkzaamheden') or None
        naaminpersen = (request.POST.get('naaminpersen') == 'on')
        behandelaar = request.POST.get('behandelaar', '')
        technicus = request.POST.get('technicus', '')
        notities = request.POST.get('notities', '')
        facturabel_garantie = request.POST.get('facturabel_garantie', '')
        
        # ----- Verwerk het NZACode veld -----
        nza_code_pk = request.POST.get('nza_code')
        nza_instance = None
        if nza_code_pk:
            try:
                nza_instance = NZACode.objects.get(pk=nza_code_pk)
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
        
        # ----- Klantdossier aanmaken indien aangevinkt -----
        if request.POST.get('create_klantdossier') == 'on':
            create_klantdossier_for_klant(klant)
        
        # ----- Bepaal de actie (Opslaan of Printen) -----
        action = request.POST.get('action', 'save')
        if action == 'print':
            return redirect(reverse('werkbon_print', args=[werkbon.pk]))
        else:
            return redirect(reverse('werkbon_detail', args=[werkbon.pk]))
    
    # Voor GET-verzoeken: haal alle beschikbare NZACodes op en geef ze mee aan de template
    nza_codes = NZACode.objects.all()
    return render(request, 'planning/form.html', {'nza_codes': nza_codes})