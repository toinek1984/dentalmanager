import json
import random
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from apps.planning.models import Werkbon

def werkbon_list(request):
    """
    Retourneert een JSON-lijst van werkbonnen.
    Het veld 'resourceId' bevat de opgeslagen behandelaar-naam en we voegen 'barcode' toe.
    """
    werkbonnen = Werkbon.objects.all()
    data = []
    for wb in werkbonnen:
        resource_val = wb.behandelaar if wb.behandelaar else None
        start_str = wb.aanvang_werkzaamheden.isoformat() if wb.aanvang_werkzaamheden else None
        data.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': start_str,
            'resourceId': resource_val,
            'barcode': wb.barcode,    # Voeg barcode toe
            'status': wb.status,
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def update_werkbon(request, pk):
    """
    Update de 'aanvang_werkzaamheden' en 'behandelaar' van een werkbon.
    Verwacht JSON met:
      - start: ISO datetime-string
      - resource: Naam van de behandelaar (string)
    """
    from django.shortcuts import get_object_or_404
    wb = get_object_or_404(Werkbon, pk=pk)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_start_str = data.get('start')
            resource = data.get('resource')
            if not new_start_str:
                return HttpResponseBadRequest("Missing field: start")
            if not resource:
                return HttpResponseBadRequest("Missing field: resource")
            try:
                new_start = datetime.fromisoformat(new_start_str.replace("Z", ""))
            except Exception as conv_error:
                return HttpResponseBadRequest("Invalid start datetime format: " + str(conv_error))
            wb.aanvang_werkzaamheden = new_start
            wb.behandelaar = resource
            wb.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid method.")

@csrf_exempt
def create_werkbon(request):
    """
    API endpoint om een nieuwe werkbon aan te maken.
    Verwacht een JSON payload met:
      - title: Titel van de werkbon (string)
      - start: ISO datetime-string (bijv. "2025-03-24T10:00:00")
      - resource: Naam van de behandelaar (string, bv. "Jellie")
    
    Om UNIQUE constraint problemen te voorkomen, voegen we een random nummer toe.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("create_werkbon received data:", data)
            title = data.get('title')
            start_str = data.get('start')
            resource = data.get('resource')
            if not title:
                return HttpResponseBadRequest("Missing field: title")
            if not start_str:
                return HttpResponseBadRequest("Missing field: start")
            if not resource:
                return HttpResponseBadRequest("Missing field: resource")
            try:
                start = datetime.fromisoformat(start_str.replace("Z", ""))
            except Exception as conv_error:
                return HttpResponseBadRequest("Invalid start datetime format: " + str(conv_error))
            # Maak een uniek werkbonnummer door een random getal toe te voegen
            unique_title = f"{title}_{random.randint(1000, 9999)}"
            wb = Werkbon.objects.create(
                werkbonnummer=unique_title,
                aanvang_werkzaamheden=start,
                behandelaar=resource,
                status='open'
            )
            print("Werkbon created with id:", wb.pk)
            return JsonResponse({'status': 'success', 'id': wb.pk})
        except Exception as e:
            print("Exception in create_werkbon:", e)
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid method.")



def api_resources(request):
    """
    Retourneert een JSON-lijst met de opties voor behandelaars (resources).
    Deze lijst komt overeen met de BEHANDELAAR_CHOICES in het model.
    """
    # Definieer de opties zoals in je modelkeuzes
    choices = [
        {'id': 'Jellie', 'title': 'Jellie'},
        {'id': 'Romy', 'title': 'Romy'},
        {'id': 'Sabrina', 'title': 'Sabrina'},
        {'id': 'Ellen', 'title': 'Ellen'},
        {'id': 'Usman', 'title': 'Usman'},
        {'id': 'Job', 'title': 'Job'},
        {'id': 'Myrthe', 'title': 'Myrthe'}, 
    ]
    
    return JsonResponse(choices, safe=False)
