from django.shortcuts import render
from apps.planning.models import Werkbon

def planboard(request):
    # Selecteer alleen werkbonnen zonder startdatum
    unscheduled = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)
    return render(request, 'planning/planboard.html', {'unscheduled_workbonnen': unscheduled})
