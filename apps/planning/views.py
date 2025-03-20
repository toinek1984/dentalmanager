from django.shortcuts import render, redirect
from django.urls import reverse
from apps.planning.models import Werkbon, Opdrachtgever
from apps.klanten.models import Klant
from apps.hr.werknemers.models import Werknemer  # Zorg dat dit correct wordt geïmporteerd
from .forms import WerkbonForm
from django.shortcuts import render, redirect, get_object_or_404
from apps.planning.models import Werkbon

def planboard(request):
    # Jouw bestaande planboard-view (als voorbeeld)
    return render(request, 'planning/planboard.html')

def planboard_resource(request):
    # Jouw bestaande resource-view
    return render(request, 'planning/planboard_resource.html')

def werkbonnen(request):
    """
    Deze view geeft een overzicht van alle werkbonnen.
    Pas de template aan naar de gewenste weergave (bijv. 'planning/werkbon_overzicht.html').
    """
    werkbon_list = Werkbon.objects.all().order_by('-aanmaakdatum')
    return render(request, 'planning/werkbon_overzicht.html', {'werkbonnen': werkbon_list})
    
def create_werkbon(request):
    if request.method == "POST":
        form = WerkbonForm(request.POST)
        if form.is_valid():
            werkbon = form.save(commit=False)

            klant_naam = request.POST.get('klant_naam')
            klant, created = Klant.objects.get_or_create(
                naam=klant_naam,
                defaults={
                    'adres': request.POST.get('klant_adres', ''),
                    'woonplaats': request.POST.get('klant_woonplaats', ''),
                    'telefoon': request.POST.get('klant_telefoon', ''),
                    'email': request.POST.get('klant_email', ''),
                    'geboortedatum': request.POST.get('klant_geboortedatum') or None,
                }
            )

            werkbon.klant = klant  
            opdrachtgever_naam = form.cleaned_data.get('opdrachtgever_naam')
            opdrachtgever = None

            if opdrachtgever_naam:
                opdrachtgever, _ = Opdrachtgever.objects.get_or_create(
                    naam=opdrachtgever_naam,
                    defaults={
                        'adres': form.cleaned_data.get('opdrachtgever_adres', ''),
                        'telefoon': form.cleaned_data.get('opdrachtgever_telefoon', ''),
                        'email': form.cleaned_data.get('opdrachtgever_email', ''),
                    }
                )

            werkbon.opdrachtgever = opdrachtgever  
            werkbon.save()

            action = request.POST.get('action', 'save')
            if action == 'print':
                return redirect(reverse('werkbon_print', args=[werkbon.pk]))
            return redirect(reverse('werkbon_detail', args=[werkbon.pk]))

    else:
        form = WerkbonForm()

    return render(request, 'planning/form.html', {'form': form})


def planboard(request):
    werknemers = Werknemer.objects.all()  # Haal alle werknemers op
    unscheduled_workbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)

    return render(request, 'planning/planboard.html', {
        'werknemers': werknemers,  # ✅ Doorsturen naar template
        'unscheduled_workbonnen': unscheduled_workbonnen
    })


def planboard_resource(request):
    """
    Laadt de resource view van de planboard, inclusief medewerkers en niet-geplande werkbonnen.
    """
    werknemers = Werknemer.objects.all()  # Haal alle werknemers op
    unscheduled_workbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)

    return render(request, 'planning/planboard_resource.html', {
        'werknemers': werknemers,
        'unscheduled_workbonnen': unscheduled_workbonnen
    })


def index(request):
    """
    Een eenvoudige startpagina voor de planning-app.
    """
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de planning app!')
