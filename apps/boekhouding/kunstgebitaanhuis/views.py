import json
from datetime import date
from django.shortcuts import render
from django.db.models import Sum
from apps.boekhouding.tarieven.models import NZACode  # Voor indien dropdown-opties nodig zijn
from apps.boekhouding.grootboekrekeningen.models import Grootboekrekening  # Directe dropdown-opties
from apps.planning.models import Werkbon  # Pas dit pad aan indien jouw Werkbon-model elders staat

def quarter_to_date_range(q, yr):
    """
    Zet kwartaal (1..4) + jaar om in een tuple (startdatum, einddatum).
    """
    q = int(q)
    yr = int(yr)
    if q == 1:
        start = date(yr, 1, 1)
        end = date(yr, 3, 31)
    elif q == 2:
        start = date(yr, 4, 1)
        end = date(yr, 6, 30)
    elif q == 3:
        start = date(yr, 7, 1)
        end = date(yr, 9, 30)
    else:
        start = date(yr, 10, 1)
        end = date(yr, 12, 31)
    return (start, end)

def aggregeer_periode(qs, start, end):
    """
    Aggregeert werkbondata binnen een periode.
      - Voor werkbonnen met facturabel_garantie 'facturabel' telt het de som van 'verkoopwaarde' (Honorarium).
      - Voor werkbonnen met facturabel_garantie 'garantie' telt het de som van 'verkoopwaarde' (als faalkosten).
    """
    data = qs.filter(aanmaakdatum__range=(start, end)).values('facturabel_garantie').annotate(
        totaal_verkoop=Sum('verkoopwaarde')
    )
    totals = {'facturabel': 0.0, 'garantie': 0.0}
    for row in data:
        key = row['facturabel_garantie'].lower()
        if key == 'facturabel':
            totals['facturabel'] += row['totaal_verkoop'] or 0
        elif key == 'garantie':
            totals['garantie'] += row['totaal_verkoop'] or 0
    return totals

def overall_inkoop(qs, start, end):
    """
    Bereken de totale inkoopwaarde binnen de periode.
    """
    agg = qs.filter(aanmaakdatum__range=(start, end)).aggregate(total_inkoop=Sum('inkoopwaarde'))
    return agg['total_inkoop'] or 0

def dashboard(request):
    # Lees GET-parameters (standaard kwartaal 1 en 2 van 2025)
    quarter1 = request.GET.get('quarter1', '1')
    year1 = request.GET.get('year1', '2025')
    quarter2 = request.GET.get('quarter2', '2')
    year2 = request.GET.get('year2', '2025')
    
    # Filter optioneel op behandelaar en grootboekrekening
    selected_behandelaar = request.GET.get('behandelaar', '')
    selected_rekening = request.GET.get('grootboekrekening', '')
    
    # Bepaal de datumbereiken
    start1, end1 = quarter_to_date_range(quarter1, year1)
    start2, end2 = quarter_to_date_range(quarter2, year2)
    
    # Haal werkbonnen op met status 'gesloten'
    werkbonnen = Werkbon.objects.filter(status='gesloten')
    if selected_behandelaar:
        werkbonnen = werkbonnen.filter(behandelaar=selected_behandelaar)
    if selected_rekening:
        werkbonnen = werkbonnen.filter(nza_code__grootboekrekening__code=selected_rekening)
    
    # Bereken totalen per periode
    tot1 = aggregeer_periode(werkbonnen, start1, end1)
    tot2 = aggregeer_periode(werkbonnen, start2, end2)
    
    # Bereken inkoopwaarden per periode
    ink1 = overall_inkoop(werkbonnen, start1, end1)
    ink2 = overall_inkoop(werkbonnen, start2, end2)
    
    # Bereken winst/verlies: winst = honorarium - garantie - inkoop
    winst1 = tot1['facturabel'] - tot1['garantie'] - ink1
    winst2 = tot2['facturabel'] - tot2['garantie'] - ink2

    # Bouw grafiekdata (vier datasets: honorarium, garantie, inkoop, winst)
    graph_data = {
        'honorarium': [tot1['facturabel'], tot2['facturabel']],
        'garantie': [tot1['garantie'], tot2['garantie']],
        'inkoop': [ink1, ink2],
        'winst': [winst1, winst2],
    }
    
    # Haal grootboekrekening-opties op voor de dropdown direct uit het Grootboekrekening-model.
    rekening_options = Grootboekrekening.objects.all().values_list('code', flat=True).distinct()
    rekening_options = list(rekening_options)
    
    context = {
        'quarter1': quarter1,
        'year1': year1,
        'quarter2': quarter2,
        'year2': year2,
        'selected_behandelaar': selected_behandelaar,
        'selected_rekening': selected_rekening,
        'totale_p1': tot1,
        'totale_p2': tot2,
        'inkoop1': ink1,
        'inkoop2': ink2,
        'winst1': winst1,
        'winst2': winst2,
        'rekening_options': rekening_options,
        'graph_data': json.dumps(graph_data),
    }
    return render(request, 'boekhouding/kunstgebitaanhuis/dashboard.html', context)
