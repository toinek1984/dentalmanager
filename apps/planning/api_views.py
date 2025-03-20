import json
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from apps.planning.models import Werkbon
from apps.hr.werknemers.models import Werknemer

def werkbon_list(request):
    """
    Retourneert een JSON-lijst van werkbonnen.
    Let op: als het veld 'behandelaar' een string bevat (bijvoorbeeld oude data),
    dan wordt er None teruggegeven als resourceId.
    """
    werkbonnen = Werkbon.objects.all()
    data = []
    for wb in werkbonnen:
        # Controleer of wb.behandelaar een object is met een 'id'-attribuut
        if wb.behandelaar and hasattr(wb.behandelaar, 'id'):
            resource_id = wb.behandelaar.id
        else:
            resource_id = None

        data.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': wb.aanvang_werkzaamheden.isoformat() if wb.aanvang_werkzaamheden else None,
            'resourceId': resource_id,
            'status': wb.status,
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def update_werkbon(request, pk):
    """
    Update de 'aanvang_werkzaamheden' van een werkbon op basis van de 'start' datum 
    uit de POST-data. Verwacht een JSON payload met onder andere de sleutel 'start'.
    """
    if request.method == "POST":
        wb = get_object_or_404(Werkbon, pk=pk)
        try:
            data = json.loads(request.body)
            new_date_str = data.get('start')
            if new_date_str:
                # Gebruik alleen het datumgedeelte (split op "T" indien aanwezig)
                new_date_str = new_date_str.split("T")[0]
                new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
                wb.aanvang_werkzaamheden = new_date
                wb.save()
                return JsonResponse({'status': 'success'})
            else:
                return HttpResponseBadRequest("Missing 'start' field.")
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid method.")

def api_resources(request):
    """
    Retourneert een JSON-lijst met alle medewerkers (werknemers) voor FullCalendar.
    Elk object bevat de 'id' en de 'title' (volledige naam).
    """
    werknemers = Werknemer.objects.all().values('id', 'naam')
    data = [{'id': w['id'], 'title': w['naam']} for w in werknemers]
    return JsonResponse(data, safe=False)
