from django.shortcuts import render, redirect
from django.urls import reverse
from apps.planning.models import Werkbon, Klant, Opdrachtgever
from apps.boekhouding.tarieven.models import NZACode

def create_werkbon(request):
    if request.method == "POST":
        # ----- Klantgegevens -----
        klant_naam = request.POST.get('klant_naam')
        klant_adres = request.POST.get('klant_adres')
        klant_woonplaats = request.POST.get('klant_woonplaats')
        klant_geboortedatum = request.POST.get('klant_geboortedatum')
        klant_telefoon = request.POST.get('klant_telefoon')
        klant_email = request.POST.get('klant_email')
        klant_verzekeringsnummer = request.POST.get('klant_verzekeringsnummer')
        mantelzorger = request.POST.get('mantelzorger') == 'on'
        mantelzorger_naam = request.POST.get('mantelzorger_naam')
        mantelzorger_telefoon = request.POST.get('mantelzorger_telefoon')
        mantelzorger_geboortedatum = request.POST.get('mantelzorger_geboortedatum')
        onder_bewind = request.POST.get('onder_bewind') == 'on'
        klant_herkomst = request.POST.get('klant_herkomst')
        
        klant, _ = Klant.objects.get_or_create(
            naam=klant_naam,
            defaults={
                'adres': klant_adres,
                'woonplaats': klant_woonplaats,
                'geboortedatum': klant_geboortedatum or None,
                'telefoon': klant_telefoon,
                'email': klant_email,
                'verzekeringsnummer': klant_verzekeringsnummer,
                'mantelzorger': mantelzorger,
                'mantelzorger_naam': mantelzorger_naam,
                'mantelzorger_telefoon': mantelzorger_telefoon,
                'mantelzorger_geboortedatum': mantelzorger_geboortedatum or None,
                'onder_bewind': onder_bewind,
                'herkomst': klant_herkomst,
            }
        )
        
        # ----- Opdrachtgevergegevens -----
        opdrachtgever_naam = request.POST.get('opdrachtgever_naam')
        opdrachtgever_adres = request.POST.get('opdrachtgever_adres')
        opdrachtgever_telefoon = request.POST.get('opdrachtgever_telefoon')
        opdrachtgever_email = request.POST.get('opdrachtgever_email')
        opdrachtgever_kvk = request.POST.get('opdrachtgever_kvk')
        opdrachtgever_contactpersoon = request.POST.get('opdrachtgever_contactpersoon')
        opdrachtgever_woonplaats = request.POST.get('opdrachtgever_woonplaats')
        
        opdrachtgever = None
        if opdrachtgever_naam:
            opdrachtgever, _ = Opdrachtgever.objects.get_or_create(
                naam=opdrachtgever_naam,
                defaults={
                    'adres': opdrachtgever_adres,
                    'telefoon': opdrachtgever_telefoon,
                    'email': opdrachtgever_email,
                    'kvk': opdrachtgever_kvk,
                    'contactpersoon': opdrachtgever_contactpersoon,
                    'woonplaats': opdrachtgever_woonplaats,
                }
            )
        
        # ----- Werkbon Specifieke Gegevens -----
        gebitsdatum = request.POST.get('gebitsdatum')
        tandkleur = request.POST.get('tandkleur')
        aanvang_werkzaamheden = request.POST.get('aanvang_werkzaamheden')
        naaminpersen = request.POST.get('naaminpersen') == 'on'
        behandelaar = request.POST.get('behandelaar')
        technicus = request.POST.get('technicus')
        notities = request.POST.get('notities')
        facturabel_garantie = request.POST.get('facturabel_garantie')
        
        # ----- Verwerk het NZA Code veld -----
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
            gebitsdatum=gebitsdatum or None,
            tandkleur=tandkleur,
            aanvang_werkzaamheden=aanvang_werkzaamheden or None,
            naaminpersen=naaminpersen,
            behandelaar=behandelaar,
            technicus=technicus,
            notities=notities,
            nza_code=nza_instance,
            facturabel_garantie=facturabel_garantie
        )
        
        action = request.POST.get('action', 'save')
        if action == 'print':
            return redirect(reverse('werkbon_print', args=[werkbon.pk]))
        else:
            return redirect(reverse('werkbon_detail', args=[werkbon.pk]))
    
    return render(request, 'planning/form.html')
