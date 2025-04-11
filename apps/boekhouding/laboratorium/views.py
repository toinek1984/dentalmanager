import json
from datetime import date
from django.shortcuts import render
from django.db.models import Sum
from apps.planning.models import Werkbon  # Pas dit pad aan indien nodig
from apps.boekhouding.tarieven.models import NZACode  # Voor andere zaken
from apps.boekhouding.grootboekrekeningen.models import Grootboekrekening  # Nieuw: voor de dropdown

def quarter_to_date_range(q, yr):
    """
    Zet kwartaal (1..4) + jaar om in (startdatum, einddatum) als date-objects.
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
    else:  # q == 4
        start = date(yr, 10, 1)
        end = date(yr, 12, 31)
    return (start, end)

def aggregeer_periode(qs, start, end):
    """
    Aggregeert werkbondata binnen een periode voor de omzet (verkoopwaarde) op basis van 'facturabel_garantie'.
    We gaan ervan uit dat:
      - 'facturabel' werkbonnen als normale omzet tellen.
      - 'garantie' als faalkosten worden gezien.
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
    Berekent de totale inkoopwaarde binnen de periode.
    """
    agg = qs.filter(aanmaakdatum__range=(start, end)).aggregate(total_inkoop=Sum('inkoopwaarde'))
    return agg['total_inkoop'] or 0

def dashboard(request):
    # Lees GET-parameters (standaard: kwartaal 1 en 2 van 2025)
    quarter1 = request.GET.get('quarter1', '1')
    year1 = request.GET.get('year1', '2025')
    quarter2 = request.GET.get('quarter2', '2')
    year2 = request.GET.get('year2', '2025')
    
    # Optioneel: filter op technicus en/of grootboekrekening
    selected_technicus = request.GET.get('technicus', '')
    selected_rekening = request.GET.get('grootboekrekening', '')
    
    # Bepaal de datumbereiken
    start1, end1 = quarter_to_date_range(quarter1, year1)
    start2, end2 = quarter_to_date_range(quarter2, year2)
    
    # Haal de werkbonnen op en filter op status 'gesloten'
    werkbonnen = Werkbon.objects.filter(status='gesloten')
    if selected_technicus:
        werkbonnen = werkbonnen.filter(technicus=selected_technicus)
    if selected_rekening:
        werkbonnen = werkbonnen.filter(nza_code__grootboekrekening__code=selected_rekening)
    
    # Bereken totalen per periode
    totale_p1 = aggregeer_periode(werkbonnen, start1, end1)
    totale_p2 = aggregeer_periode(werkbonnen, start2, end2)
    
    # Bereken inkoop voor beide perioden
    inkoop1 = overall_inkoop(werkbonnen, start1, end1)
    inkoop2 = overall_inkoop(werkbonnen, start2, end2)
    
    # Bereken winst/verlies: winst = facturabel - garantie - inkoop
    winst1 = totale_p1['facturabel'] - totale_p1['garantie'] - inkoop1
    winst2 = totale_p2['facturabel'] - totale_p2['garantie'] - inkoop2

    # Bouw data voor grafieken: vier grafieken voor facturabel, garantie, inkoop, winst
    graph_data = {
        'facturabel': [totale_p1['facturabel'], totale_p2['facturabel']],
        'garantie': [totale_p1['garantie'], totale_p2['garantie']],
        'inkoop': [inkoop1, inkoop2],
        'winst': [winst1, winst2],
    }
    
    # Haal alle grootboekrekening-opties op voor de dropdown via het Grootboekrekening-model
    rekening_options = Grootboekrekening.objects.all().values_list('code', flat=True).distinct()
    rekening_options = list(rekening_options)
    
    context = {
        'quarter1': quarter1,
        'year1': year1,
        'quarter2': quarter2,
        'year2': year2,
        'selected_technicus': selected_technicus,
        'selected_rekening': selected_rekening,
        'totale_p1': totale_p1,
        'totale_p2': totale_p2,
        'inkoop1': inkoop1,
        'inkoop2': inkoop2,
        'winst1': winst1,
        'winst2': winst2,
        'rekening_options': rekening_options,
        'graph_data': json.dumps(graph_data),
    }
    return render(request, 'boekhouding/laboratorium/dashboard.html', context)
