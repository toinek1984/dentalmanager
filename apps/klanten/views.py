from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Klant
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from apps.klanten.klantdossier.models import KlantDossier
from .forms import KlantDossierForm
from django.utils import timezone
from .forms import KlantNotitieForm 
from django.http import JsonResponse
from .models import Klant
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    ...

def search_klant(request):
    """Zoekt klanten op basis van een zoekterm en geeft een JSON-lijst terug."""
    zoekterm = request.GET.get('q', '').strip()
    klanten = Klant.objects.filter(naam__icontains=zoekterm).values('id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email')
    return JsonResponse(list(klanten), safe=False)


def klantenoverzicht(request):
    try:
        klanten = Klant.objects.all()
        return render(request, 'klanten/klantenoverzicht.html', {'klanten': klanten})
    except Exception as e:
        print(f"❌ Fout in klantenoverzicht: {e}")
        return HttpResponse(f"Er is een fout opgetreden: {e}", status=500)

# Voeg deze toe als hij ontbreekt
def index(request):
    return render(request, 'klanten/index.html')  # Zorg dat index.html bestaat!
    
def klanten_json(request):
    q = request.GET.get('q', '')
    klanten = Klant.objects.filter(naam__icontains=q).values('id', 'naam', 'adres', 'woonplaats', 'telefoon', 'email')
    return JsonResponse(list(klanten), safe=False)    
    
def dossier_create(request):
    if request.method == 'POST':
        form = KlantDossierForm(request.POST)
        if form.is_valid():
            dossier = form.save()
            return redirect(reverse('klanten:dossier_detail', args=[dossier.klantnummer]))
    else:
        form = KlantDossierForm()
    return render(request, 'klanten/dossier_form.html', {'form': form})    

def open_werkbon_form(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    # Hier kun je de werkbon-functionaliteit integreren.
    # Voor nu renderen we een placeholder template.
    return render(request, 'klanten/werkbon_form.html', {'dossier': dossier})
    
def mark_overleden(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    if request.method == 'POST':
        dossier.is_overleden = True
        dossier.overlijdensdatum = timezone.now().date()
        dossier.save()
        return redirect(reverse('klanten:dossier_detail', args=[dossier.klantnummer]))
    return render(request, 'klanten/confirm_overleden.html', {'dossier': dossier})    



def dossier_list(request):
    dossiers = KlantDossier.objects.all().order_by('-created_at')
    return render(request, 'klanten/dossier_list.html', {'dossiers': dossiers})

def dossier_detail(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    note_form = KlantNotitieForm()
    
    if request.method == 'POST' and 'add_note' in request.POST:
        note_form = KlantNotitieForm(request.POST)
        if note_form.is_valid():
            notitie = note_form.save(commit=False)
            notitie.dossier = dossier
            notitie.save()
            return redirect(reverse('klanten:dossier_detail', args=[dossier.klantnummer]))
    
    return render(request, 'klanten/dossier_detail.html', {'dossier': dossier, 'note_form': note_form})

def dossier_edit(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    if request.method == 'POST':
        form = KlantDossierForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            return redirect(reverse('klanten:dossier_detail', args=[dossier.klantnummer]))
    else:
        form = KlantDossierForm(instance=dossier)
    return render(request, 'klanten/dossier_edit.html', {'form': form, 'dossier': dossier})

def mark_overleden(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    if request.method == 'POST':
        dossier.is_overleden = True
        from django.utils import timezone
        dossier.overlijdensdatum = timezone.now().date()
        dossier.save()
        return redirect(reverse('klanten:dossier_detail', args=[dossier.klantnummer]))
    return render(request, 'klanten/confirm_overleden.html', {'dossier': dossier})

# Je open werkbon view kan bijvoorbeeld zo zijn:
def open_werkbon_form(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    return render(request, 'klanten/werkbon_form.html', {'dossier': dossier})
    
def add_notitie(request, klantnummer):
    dossier = get_object_or_404(KlantDossier, klantnummer=klantnummer)
    if request.method == 'POST':
        form = KlantNotitieForm(request.POST)
        if form.is_valid():
            notitie = form.save(commit=False)
            notitie.dossier = dossier
            notitie.save()
            return redirect(reverse('klanten:dossier_detail', args=[dossier.klantnummer]))
    else:
        form = KlantNotitieForm()
    return render(request, 'klanten/add_notitie.html', {'form': form, 'dossier': dossier})    
    
    
# In apps/klanten/views.py
def klantaanmaken(request):
    # Hier zou je een formulier voor klantaanmaken verwerken
    # Voorbeeld: render een template met een leeg formulier
    return render(request, 'klanten/klantaanmaken.html')
    