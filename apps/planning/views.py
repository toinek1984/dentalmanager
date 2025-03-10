
from apps.planning.models import Werkbon
# apps/planning/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from apps.planning.models import Werkbon, Klant, Opdrachtgever
from .forms import WerkbonForm

def create_werkbon(request):
    """
    Maakt een nieuwe werkbon aan via een formulier.
    Zorg dat het formulier (WerkbonForm) in apps/planning/forms.py gedefinieerd is.
    Dit formulier bevat onder andere het NZACode-veld (als ModelChoiceField).
    """
    if request.method == "POST":
        form = WerkbonForm(request.POST)
        if form.is_valid():
            werkbon = form.save()
            action = request.POST.get('action', 'save')
            if action == 'print':
                # Zorg dat de URL 'werkbon_print' in je URL-configuratie staat
                return redirect(reverse('werkbon_print', args=[werkbon.pk]))
            else:
                # Zorg dat de URL 'werkbon_detail' in je URL-configuratie staat
                return redirect(reverse('werkbon_detail', args=[werkbon.pk]))
    else:
        form = WerkbonForm()
    return render(request, 'planning/form.html', {'form': form})


def planboard(request):
    """
    Toont de planboard voor werkbonnen die nog niet gepland (aanvang_werkzaamheden is NULL) zijn.
    """
    unscheduled_workbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)
    return render(request, 'planning/planboard.html', {'unscheduled_workbonnen': unscheduled_workbonnen})


def planboard_resource(request):
    """
    Toont de resource-weergave van de planboard.
    """
    unscheduled_workbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)
    return render(request, 'planning/planboard_resource.html', {'unscheduled_workbonnen': unscheduled_workbonnen})


def index(request):
    """
    Een eenvoudige startpagina voor de planning-app.
    """
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de planning app!')
