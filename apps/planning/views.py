from django.shortcuts import render, redirect
from django.urls import reverse
from apps.planning.models import Werkbon, Opdrachtgever
from apps.klanten.models import Klant
from apps.hr.werknemers.models import Werknemer  # Zorg dat dit correct wordt geïmporteerd
from .forms import WerkbonForm

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
