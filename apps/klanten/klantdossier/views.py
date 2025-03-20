from django.shortcuts import render, get_object_or_404
from apps.klanten.models import Klant  # Of importeer het relevante model

def dossier_detail(request, klant_id):
    # Haal de klant of dossier op op basis van het ID
    klant = get_object_or_404(Klant, id=klant_id)
    return render(request, 'klanten/klantdossier/detail.html', {'klant': klant})
