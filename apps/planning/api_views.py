import json
import random
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from apps.planning.models import Werkbon
from dateutil import parser
# Zorg dat hier geen dubbele import van JsonResponse gebeurt

def api_resources(request):
    """
    Retourneert een JSON-lijst met de opties voor behandelaars (resources).
    Deze lijst komt overeen met de BEHANDELAAR_CHOICES in het model.
    """
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

# def api_werkbonnen(request):
    # start = request.GET.get('start')
    # end = request.GET.get('end')
    # if start and end:
        # try:
            # Gebruik fuzzy=True zodat overtollige componenten genegeerd worden
            # start_date = parser.parse(start, fuzzy=True).date()
            # end_date = parser.parse(end, fuzzy=True).date()
        # except Exception as e:
            # return HttpResponseBadRequest("Invalid date format: " + str(e))
        # werkbonnen = Werkbon.objects.filter(
            # aanmaakdatum__gte=start_date,
            # aanmaakdatum__lte=end_date,
            # status__in=['open', 'gepland']
        # )
    # else:
        # werkbonnen = Werkbon.objects.filter(status__in=['open', 'gepland'])
    # data = [{
        # 'id': wb.id,
        # 'title': wb.werkbonnummer,
        # 'start': wb.aanvang_werkzaamheden.isoformat() if wb.aanvang_werkzaamheden else None,
        # 'status': wb.status,
        # 'barcode': wb.barcode,
    # } for wb in werkbonnen]
    # return JsonResponse(data, safe=False)
    
    
def werkbon_list(request):
    """
    Retourneert een JSON-lijst van werkbonnen inclusief velden zoals resourceId (behandelaar-naam), barcode en status.
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
            'barcode': wb.barcode,    # Barcode toegevoegd
            'status': wb.status,
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def update_werkbon(request, pk):
    """
    Update de 'aanvang_werkzaamheden' en de behandelaar van een werkbon.
    Verwacht JSON met:
      - start: ISO datetime-string
      - resource: Naam van de behandelaar (string)
    """
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
                # Zorg ervoor dat het formaat correct is
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
      - start: ISO datetime-string
      - resource: Naam van de behandelaar (string)
    Voeg een random nummer toe om te zorgen voor een uniek werkbonnummer.
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
