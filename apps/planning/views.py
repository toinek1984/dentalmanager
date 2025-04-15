from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
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

def print_werkbon(request, pk):
    werkbon = get_object_or_404(Werkbon, pk=pk)
    return render(request, 'planning/print.html', {'werkbon': werkbon})
    
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

def employee_overview(request):
    """
    Geeft een overzicht van de werkbonnen, zowel globaal als per werknemer,
    gegroepeerd naar dag, week en maand.
    """
    # Globaal overzicht over alle werkbonnen die een starttijd hebben
    global_daily = (
        Werkbon.objects.filter(aanvang_werkzaamheden__isnull=False)
        .annotate(day=TruncDay('aanvang_werkzaamheden'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    global_weekly = (
        Werkbon.objects.filter(aanvang_werkzaamheden__isnull=False)
        .annotate(week=TruncWeek('aanvang_werkzaamheden'))
        .values('week')
        .annotate(count=Count('id'))
        .order_by('week')
    )
    global_monthly = (
        Werkbon.objects.filter(aanvang_werkzaamheden__isnull=False)
        .annotate(month=TruncMonth('aanvang_werkzaamheden'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Overzicht per werknemer:
    # Aangezien in de werkbon als 'technicus' de volledige naam wordt opgeslagen,
    # construeren we de volledige naam uit de velden voornaam en achternaam.
    employees = Werknemer.objects.all()
    overview = {}
    for employee in employees:
        fullname = f"{employee.voornaam} {employee.achternaam}"
        daily = (
            Werkbon.objects.filter(aanvang_werkzaamheden__isnull=False, technicus=fullname)
            .annotate(day=TruncDay('aanvang_werkzaamheden'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        weekly = (
            Werkbon.objects.filter(aanvang_werkzaamheden__isnull=False, technicus=fullname)
            .annotate(week=TruncWeek('aanvang_werkzaamheden'))
            .values('week')
            .annotate(count=Count('id'))
            .order_by('week')
        )
        monthly = (
            Werkbon.objects.filter(aanvang_werkzaamheden__isnull=False, technicus=fullname)
            .annotate(month=TruncMonth('aanvang_werkzaamheden'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        overview[employee.id] = {
            'fullname': fullname,
            'daily': list(daily),
            'weekly': list(weekly),
            'monthly': list(monthly),
        }

    context = {
        'global_daily': list(global_daily),
        'global_weekly': list(global_weekly),
        'global_monthly': list(global_monthly),
        'employees': employees,
        'overview': overview,
    }
    return render(request, 'planning/employee_overview.html', context)
    
   