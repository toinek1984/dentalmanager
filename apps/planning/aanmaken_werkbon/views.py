import random
import json
from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Importeer het Klant-model en Opdrachtgever vanuit de klanten-app
from apps.klanten.models import Klant, Opdrachtgever
# Overige modellen en functies
from apps.planning.models import Werkbon, generate_werkbonnummer
from apps.boekhouding.tarieven.models import NZACode
from apps.hr.werknemers.models import Werknemer
from apps.planning.forms import WerkbonForm

# -------------------------------------------------------------------
# AJAX Zoekfuncties
# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# Helper: Creëer KlantDossier voor een Klant
# -------------------------------------------------------------------
def create_klantdossier_for_klant(klant):
    """
    Zorgt dat er een KlantDossier bestaat voor de gegeven klant.
    Debugt het type en de inhoud van 'klant'.
    """
    print("DEBUG: Klant type:", type(klant))
    print("DEBUG: Klant:", klant)
    
    from apps.klanten.klantdossier.models import KlantDossier
    dossier, created = KlantDossier.objects.get_or_create(klant=klant)
    if created:
        print(f"Klantdossier aangemaakt voor: {klant}")
    else:
        print(f"Klantdossier bestaat al voor: {klant}")
    return dossier

# -------------------------------------------------------------------
# Overige Views
# -------------------------------------------------------------------
def index(request):
    return HttpResponse('Welkom bij de planning app!')

def planboard(request):
    werknemers = Werknemer.objects.all()
    unscheduled_workbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)
    return render(request, 'planning/planboard.html', {
        'werknemers': werknemers,
        'unscheduled_workbonnen': unscheduled_workbonnen
    })

def planboard_resource(request):
    werknemers = Werknemer.objects.all()
    unscheduled_workbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)
    return render(request, 'planning/planboard_resource.html', {
        'werknemers': werknemers,
        'unscheduled_workbonnen': unscheduled_workbonnen
    })

def werkbonnen(request):
    werkbon_list = Werkbon.objects.all().order_by('-aanmaakdatum')
    return render(request, 'planning/werkbon_overzicht.html', {'werkbonnen': werkbon_list})

def print_werkbon(request, pk):
    werkbon = get_object_or_404(Werkbon, pk=pk)
    return render(request, 'planning/print.html', {'werkbon': werkbon})

# -------------------------------------------------------------------
# View: Aanmaken van een nieuwe Werkbon
# -------------------------------------------------------------------
def create_werkbon(request):
    """
    Verwerkt een POST-request om een nieuwe werkbon aan te maken.
    Combineert de klantvelden (voornaam en achternaam) tot één volledige naam
    en verwerkt de overige velden.
    """
    if request.method == "POST":
        # Klantgegevens: aparte velden voor voornaam en achternaam.
        klant_voornaam = request.POST.get('klant_voornaam', '').strip()
        klant_achternaam = request.POST.get('klant_achternaam', '').strip()
        if not klant_voornaam or not klant_achternaam:
            return HttpResponseBadRequest("Zowel voornaam als achternaam van de klant zijn verplicht.")
        klant_volledige_naam = f"{klant_voornaam} {klant_achternaam}"
        
        # Overige klantgegevens
        klant_adres = request.POST.get('klant_adres', '').strip()
        klant_woonplaats = request.POST.get('klant_woonplaats', '').strip()
        klant_geboortedatum = request.POST.get('klant_geboortedatum') or None
        klant_telefoon = request.POST.get('klant_telefoon', '').strip()
        klant_email = request.POST.get('klant_email', '').strip()
        klant_verzekeringsnummer = request.POST.get('klant_verzekeringsnummer', '').strip()
        
        # Haal of maak de klant op via het centrale Klant-model (uit apps/klanten/models.py)
        klant, created = Klant.objects.get_or_create(
            naam=klant_volledige_naam,
            defaults={
                'adres': klant_adres,
                'woonplaats': klant_woonplaats,
                'geboortedatum': klant_geboortedatum,
                'telefoon': klant_telefoon,
                'email': klant_email,
                'verzekeringsnummer': klant_verzekeringsnummer,
            }
        )
        print("DEBUG: Klant uit get_or_create:", klant, type(klant))
        if created:
            create_klantdossier_for_klant(klant)
        
        # Opdrachtgevergegevens
        opdrachtgever_naam = request.POST.get('opdrachtgever_naam', '').strip()
        opdrachtgever = None
        if opdrachtgever_naam:
            opdrachtgever = Opdrachtgever.objects.filter(naam__iexact=opdrachtgever_naam).first()
            if not opdrachtgever:
                opdrachtgever = Opdrachtgever.objects.create(
                    naam=opdrachtgever_naam,
                    adres=request.POST.get('opdrachtgever_adres', '').strip(),
                    telefoon=request.POST.get('opdrachtgever_telefoon', '').strip(),
                    email=request.POST.get('opdrachtgever_email', '').strip()
                )
        
        # Werkbon-specifieke gegevens
        gebitsdatum = request.POST.get('gebitsdatum') or None
        tandkleur = request.POST.get('tandkleur', '').strip()
        aanvang_werkzaamheden = None  # Wordt later ingesteld
        naaminpersen = (request.POST.get('naaminpersen') == 'on')
        
        # Medewerker-ID's voor behandelaar en technicus (vanuit het formulier als id's)
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
        
        # Controleer of de werknemers de velden voornaam en achternaam hebben
        if not (behandelaar.voornaam and behandelaar.achternaam):
            return HttpResponseBadRequest("De geselecteerde behandelaar heeft geen volledige naam.")
        if not (technicus.voornaam and technicus.achternaam):
            return HttpResponseBadRequest("De geselecteerde technicus heeft geen volledige naam.")
        
        # Combineer de volledige namen voor opslag
        behandelaar_fullname = f"{behandelaar.voornaam} {behandelaar.achternaam}"
        technicus_fullname = f"{technicus.voornaam} {technicus.achternaam}"
        
        notities = request.POST.get('notities', '').strip()
        facturabel_garantie = request.POST.get('facturabel_garantie', '').strip()
        
        # Verwerk het NZACode veld (als een nummer)
        nza_code_pk = request.POST.get('nza_code', '').strip()
        nza_instance = None
        if nza_code_pk.isdigit():
            try:
                nza_instance = NZACode.objects.get(pk=int(nza_code_pk))
            except NZACode.DoesNotExist:
                nza_instance = None
        
        # Genereer een uniek werkbonnummer
        base_werkbonnummer = generate_werkbonnummer()
        werkbonnummer = f"{base_werkbonnummer}_{random.randint(1000, 9999)}"
        
        # Maak de werkbon aan
        werkbon = Werkbon.objects.create(
           #klant=klant 
            opdrachtgever=opdrachtgever,
            gebitsdatum=gebitsdatum,
            tandkleur=tandkleur,
            aanvang_werkzaamheden=aanvang_werkzaamheden,
            naaminpersen=naaminpersen,
            behandelaar=behandelaar_fullname,
            technicus=technicus_fullname,
            notities=notities,
            nza_code=nza_instance,
            facturabel_garantie=facturabel_garantie,
            werkbonnummer=werkbonnummer
        )
        
        # Debug: Print werkbonnummer of barcode indien aanwezig
        if hasattr(werkbon, 'barcode'):
            print("Werkbon aangemaakt met barcode:", werkbon.barcode)
        else:
            print("Werkbon aangemaakt met werkbonnummer:", werkbonnummer)
        
        # Redirect op basis van de actie ("print" of "save")
        if request.POST.get('action') == 'print':
            return redirect(reverse('planning:werkbon_print', args=[werkbon.pk]))
        else:
            return redirect(reverse('planning:planboard'))
    
    else:
        form = WerkbonForm()
        nza_codes = NZACode.objects.all()
        werknemers = Werknemer.objects.all()
        context = {
            'form': form,
            'nza_codes': nza_codes,
            'werknemers': werknemers,
        }
        return render(request, 'planning/form.html', context)

# -------------------------------------------------------------------
# View: Bewerken van een bestaande Werkbon
# -------------------------------------------------------------------
def edit_werkbon(request, pk):
    werkbon = get_object_or_404(Werkbon, pk=pk)
    if request.method == "POST":
        form = WerkbonForm(request.POST, instance=werkbon)
        if form.is_valid():
            form.save()
            return redirect(reverse('planning:werkbon_overzicht'))
        else:
            return render(request, 'planning/edit_werkbon.html', {'form': form, 'werkbon': werkbon})
    else:
        form = WerkbonForm(instance=werkbon)
    return render(request, 'planning/edit_werkbon.html', {'form': form, 'werkbon': werkbon})


# -------------------------------------------------------------------
# API Endpoint: Update Werkbon (voor mobiele scanners, etc.)
# -------------------------------------------------------------------
@csrf_exempt
def update_workbon(request):
    """
    Update de werkbon-status via een POST-request met een JSON-payload.
    Voorbeeld JSON:
    {
       "werkbon_id": "123",
       "action": "fase_afgerond"  // of "gereed"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            werkbon_id = data.get('werkbon_id')
            action = data.get('action')
            
            werkbon = Werkbon.objects.get(pk=werkbon_id)
            
            if action == 'fase_afgerond':
                werkbon.status = 'fase_afgerond'
            elif action == 'gereed':
                werkbon.status = 'gereed'
            else:
                return JsonResponse({'success': False, 'message': f'Onbekende actie: {action}'}, status=400)
            
            werkbon.save()
            return JsonResponse({'success': True, 'message': 'Werkbon status succesvol bijgewerkt'})
        except Werkbon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Werkbon niet gevonden'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Fout: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Gebruik een POST-request'}, status=400)
