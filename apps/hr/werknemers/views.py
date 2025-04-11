import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Werknemer
from .forms import WerknemerForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from apps.planning.models import Werkbon  # Zorg dat dit pad klopt in jouw project

def werknemer_index(request):
    werknemers = Werknemer.objects.all()
    return render(request, 'hr/werknemers/index.html', {'werknemers': werknemers})

def werknemer_detail(request, pk):
    werknemer = get_object_or_404(Werknemer, pk=pk)
    return render(request, 'hr/werknemers/detail.html', {'werknemer': werknemer})

def werknemer_add(request):
    if request.method == 'POST':
        form = WerknemerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('werknemers:index')
    else:
        form = WerknemerForm()
    return render(request, 'hr/werknemers/form.html', {'form': form})

def werknemer_edit(request, pk):
    werknemer = get_object_or_404(Werknemer, pk=pk)
    if request.method == 'POST':
        form = WerknemerForm(request.POST, instance=werknemer)
        if form.is_valid():
            form.save()
            return redirect('werknemers:index')
    else:
        form = WerknemerForm(instance=werknemer)
    return render(request, 'hr/werknemers/form.html', {'form': form, 'werknemer': werknemer})

def werknemer_toevoegen(request):
    if request.method == 'POST':
        form = WerknemerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('werknemers:werknemer_index')
    else:
        form = WerknemerForm()
    return render(request, 'hr/werknemers/form.html', {'form': form})
    
def werknemer_insights(request, pk):
    """
    Deze view geeft per werknemer inzicht in de gewerkte uren en omzet per maand.
    We aggregeren de werkbonnen (bij status 'gesloten') per maand en vermenigvuldigen
    de totalen met het uurloon van de werknemer.
    """
    werknemer = get_object_or_404(Werknemer, pk=pk)
    
    # Filter werkbonnen voor deze werknemer met status 'gesloten'
    werkbonnen = Werkbon.objects.filter(technicus=werknemer, status='gesloten')
    
    # Aggregeer per maand (gebruik het veld 'aanmaakdatum' en ga ervan uit dat 'aantal_uren' aanwezig is)
    monthly_data = werkbonnen.annotate(month=TruncMonth('aanmaakdatum')) \
                             .values('month') \
                             .annotate(total_hours=Sum('aantal_uren')) \
                             .order_by('month')
    
    # Maak lijsten voor labels (maand) en omzet (uren * uurloon)
    labels = []
    revenues = []
    for entry in monthly_data:
        # Formatteer de datum, bijvoorbeeld als "2025-03"
        if entry['month']:
            labels.append(entry['month'].strftime("%Y-%m"))
        else:
            labels.append("Onbekend")
        total_hours = entry['total_hours'] or 0
        revenue = float(total_hours) * float(werknemer.uurloon)
        revenues.append(revenue)
    
    context = {
        'werknemer': werknemer,
        'monthly_data_labels': json.dumps(labels),
        'monthly_data_revenues': json.dumps(revenues),
    }
    return render(request, 'hr/werknemers/insights.html', context)    