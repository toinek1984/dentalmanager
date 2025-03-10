from django.shortcuts import render, redirect
from django.db.models import Sum, ExpressionWrapper, DecimalField, Count
from django.utils import timezone
from datetime import timedelta
from apps.planning.models import Werkbon
from .models import MarketingCampagne
from .forms import MarketingCampagneForm
from django.db import models  # Zorg dat we Q kunnen gebruiken
from .models import MarketingCampagne, Provincie  # Voeg Provincie toe voor filtering

def marketing_history(request):
    # Bepaal de huidige datum
    today = timezone.now().date()

    # Begin met alle campagnes die historisch zijn: 
    # Campagnes met een einddatum in het verleden of handmatig gearchiveerd
    campagnes = MarketingCampagne.objects.all().filter(
        models.Q(einddatum__isnull=False, einddatum__lt=today) | models.Q(archived=True)
    )

    # Haal filters op uit de GET-parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')
    strategie = request.GET.get('strategie')
    provincie = request.GET.get('provincie')

    if start_date:
        campagnes = campagnes.filter(startdatum__gte=start_date)
    if end_date:
        campagnes = campagnes.filter(einddatum__lte=end_date)
    if min_budget:
        campagnes = campagnes.filter(budget__gte=min_budget)
    if max_budget:
        campagnes = campagnes.filter(budget__lte=max_budget)
    if strategie:
        campagnes = campagnes.filter(strategie=strategie)
    if provincie:
        campagnes = campagnes.filter(provincie__naam=provincie)

    # Voor de dropdown in het template: haal alle provincies op
    provinces = Provincie.objects.all()

    context = {
        'campaigns': campagnes,
        'filters': {
            'start_date': start_date,
            'end_date': end_date,
            'min_budget': min_budget,
            'max_budget': max_budget,
            'strategie': strategie,
            'provincie': provincie,
        },
        'provinces': provinces,
    }
    return render(request, 'boekhouding/marketing/history.html', context)

def marketing_index(request):
    # Haal alle actieve, niet-gearchiveerde campagnes op
    campagnes = MarketingCampagne.objects.filter(actief=True, archived=False)
    return render(request, 'boekhouding/marketing/index.html', {'campagnes': campagnes})

def marketing_add(request):
    if request.method == 'POST':
        form = MarketingCampagneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marketing_index')
    else:
        form = MarketingCampagneForm()
    return render(request, 'boekhouding/marketing/add.html', {'form': form})

def marketing_dashboard(request):
    # Bepaal de huidige week (maandag tot zondag)
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)

    # Filter werkbonnen binnen deze week met een gekoppelde marketingcampagne
    werkbon_data = Werkbon.objects.filter(
        aanmaakdatum__gte=start_week,
        aanmaakdatum__lte=end_week,
        marketing_optie__isnull=False
    ).values(
        'marketing_optie__naam',
        'marketing_optie__provincie__naam'
    ).annotate(
        totaal_verkoop=Sum('verkoopwaarde'),
        totaal_inkoop=Sum('inkoopwaarde'),
        winst=ExpressionWrapper(
            Sum('verkoopwaarde') - Sum('inkoopwaarde'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ),
        aantal_werkbonnen=Count('id'),
        aantal_klanten=Count('klant', distinct=True)
    )

    context = {
        'start_week': start_week,
        'end_week': end_week,
        'werkbon_data': werkbon_data,
    }
    return render(request, 'boekhouding/marketing/dashboard.html', context)
