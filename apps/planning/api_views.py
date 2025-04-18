# apps/planning/api_views.py

import json
import random
from datetime import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from apps.planning.models import Werkbon
from apps.hr.werknemers.models import Werknemer


def api_resources(request):
    """
    Retourneert de lijst van medewerkers als resources.
    resource.id én resource.title zijn hier beide de naam-string.
    """
    medewerkers = Werknemer.objects.all()
    data = [
        {
            'id': f"{m.voornaam} {m.achternaam}",
            'title': f"{m.voornaam} {m.achternaam}"
        }
        for m in medewerkers
    ]
    return JsonResponse(data, safe=False)


def werkbon_list(request):
    """
    Retourneert alle Werkbonnen in de gevraagde periode (indien meegegeven),
    inclusief klantnaam, barcode en resourceId = behandelaar-string.
    """
    start = request.GET.get('start')
    end   = request.GET.get('end')
    qs = Werkbon.objects.all()

    if start and end:
        try:
            sd = datetime.fromisoformat(start.rstrip('Z'))
            ed = datetime.fromisoformat(end.rstrip('Z'))
            qs = qs.filter(
                aanvang_werkzaamheden__gte=sd,
                aanvang_werkzaamheden__lte=ed
            )
        except ValueError:
            # bij parse-fout: toon gewoon alles
            pass

    events = []
    for wb in qs:
        events.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': wb.aanvang_werkzaamheden.isoformat() if wb.aanvang_werkzaamheden else None,
            'resourceId': wb.behandelaar or None,
            'barcode': wb.barcode,
            'client': wb.klant.naam if wb.klant else None,
        })
    return JsonResponse(events, safe=False)

@csrf_exempt
def werkbon_update(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid method")

    try:
        data = json.loads(request.body.decode('utf-8'))
        new_start_str = data.get('start')
        new_res_str   = data.get('resourceId')
        if not new_start_str or not new_res_str:
            return HttpResponseBadRequest("Missing field: start or resourceId")

        # Parse de nieuwe starttijd (strip Z)
        try:
            new_start = datetime.fromisoformat(new_start_str.rstrip('Z'))
        except ValueError:
            return HttpResponseBadRequest("Invalid datetime format")

        # Werkbon ophalen en bijwerken
        wb = get_object_or_404(Werkbon, pk=pk)
        wb.aanvang_werkzaamheden = new_start
        wb.behandelaar = new_res_str
        wb.save()

        # *** Belangrijk: return precies status 'ok' ***
        return JsonResponse({'status': 'ok'})

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(str(e))


@csrf_exempt
def api_create_werkbon(request):
    """
    Maakt een nieuwe Werkbon aan.
    Verwacht JSON:
      {
        "title": "Vrije dag",
        "start": "2025-04-18T09:00:00Z",
        "resource": "Jellie Janssen"
      }
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid method")

    try:
        data  = json.loads(request.body.decode('utf-8'))
        title = data.get('title')
        start = data.get('start')
        res   = data.get('resource')
        if not title or not start or not res:
            return HttpResponseBadRequest("Missing field: title, start or resource")

        # Parse de start-tijd
        try:
            dt = datetime.fromisoformat(start.rstrip('Z'))
        except ValueError:
            return HttpResponseBadRequest("Invalid datetime format")

        # Maak uniek werkbonnummer
        unique_title = f"{title}_{random.randint(1000, 9999)}"

        wb = Werkbon.objects.create(
            werkbonnummer          = unique_title,
            aanvang_werkzaamheden = dt,
            behandelaar           = res,
            status                = 'open'
        )
        return JsonResponse({'status':'success','id': wb.pk})

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(str(e))
