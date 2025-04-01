from django.shortcuts import render, get_object_or_404
from .models import KlantDossier

def dossier_detail(request, klant_id):
    dossier = get_object_or_404(KlantDossier, klant__id=klant_id)
    return render(request, 'klantdossier/dossier_detail.html', {'dossier': dossier})
