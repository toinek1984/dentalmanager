# apps/planning/api_views.py

import json
import random
from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from apps.planning.models import Werkbon


# apps/planning/api_views.py

def api_resources(request):
    from apps.hr.werknemers.models import Werknemer
    data = [
        {
          'id': f"{w.voornaam} {w.achternaam}",  # óók a string
          'title': f"{w.voornaam} {w.achternaam}"
        }
        for w in Werknemer.objects.all()
    ]
    return JsonResponse(data, safe=False)



def werkbon_list(request):
    """
    Retourneert álle werkbonnen binnen eventuele start/end params,
    inclusief klantnaam en barcode.
    resourceId is de exacte string uit wb.behandelaar,
    zodat FullCalendar hem kan matchen aan een resource.id = dezelfde string.
    """
    start = request.GET.get('start')
    end   = request.GET.get('end')
    qs = Werkbon.objects.all()

    if start and end:
        try:
            # strip trailing Z en parse
            sd = datetime.fromisoformat(start.rstrip('Z'))
            ed = datetime.fromisoformat(end.rstrip('Z'))
            qs = qs.filter(
                aanvang_werkzaamheden__gte=sd,
                aanvang_werkzaamheden__lte=ed
            )
        except ValueError:
            # laat alle werkbonnen zien als parse faalt
            pass

    events = []
    for wb in qs:
        events.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': wb.aanvang_werkzaamheden.isoformat() if wb.aanvang_werkzaamheden else None,
            'resourceId': wb.behandelaar or None,          # ← string matching your resource.id
            'barcode': wb.barcode,
            'client': wb.klant.naam if wb.klant else None,  # klantnaam erbij
        })
    return JsonResponse(events, safe=False)  

@csrf_exempt
def werkbon_update(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method.")
    data = json.loads(request.body)
    new_start = data.get("start")
    new_resource = data.get("resourceId")
    if not new_start or new_resource is None:
        return HttpResponseBadRequest("Missing start or resourceId")
    dt = parse_datetime(new_start)
    if not dt:
        return HttpResponseBadRequest("Invalid datetime")
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())

    wb = get_object_or_404(Werkbon, pk=pk)
    wb.aanvang_werkzaamheden = dt
    wb.resource_id = new_resource
    wb.save()
    return JsonResponse({"status":"ok"})



@csrf_exempt
def api_create_werkbon(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method.")
    data = json.loads(request.body)
    start_str = data.get('start')
    # ...
    parsed = parse_datetime(start_str)
    if not parsed:
        return HttpResponseBadRequest("Invalid datetime format")
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())

    wb = Werkbon.objects.create(
        werkbonnummer         = unique_title,
        aanvang_werkzaamheden = parsed,
        # ...
    )
    # ...

