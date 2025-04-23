# apps/planning/api_views.py
from django.views.decorators.http import require_POST
import json
import random
from datetime import datetime, timezone
from django.utils.timezone import make_aware, is_naive
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from apps.planning.models import Werkbon
from apps.hr.werknemers.models import Werknemer
from django.utils.dateparse import parse_datetime
# =====================
# GEHEIME API TOKEN
# =====================
API_ACCESS_TOKEN = "MIJNVEILIGETOKEN123"  # wijzig deze naar wens

def is_valid_token(request):
    """Controleer of token geldig is."""
    return request.GET.get("token") == API_ACCESS_TOKEN

# =====================
# Medewerkers als resources (FullCalendar)
# =====================
def api_resources(request):
    medewerkers = Werknemer.objects.all()
    data = [
        {
            'id': f"{m.voornaam} {m.achternaam}",
            'title': f"{m.voornaam} {m.achternaam}"
        }
        for m in medewerkers
    ]
    return JsonResponse(data, safe=False)

# =====================
# Alle geplande werkbonnen (optioneel gefilterd op start/eind)
# =====================
def werkbon_list(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    print(f"[API] Werkbon-filter ontvangen: start={start}, end={end}")

    qs = Werkbon.objects.exclude(status__in=['gesloten', 'gereed'])

    if start and end:
        try:
            start_dt = parse_datetime(start)
            end_dt = parse_datetime(end)

            if is_naive(start_dt):
                start_dt = make_aware(start_dt)
            if is_naive(end_dt):
                end_dt = make_aware(end_dt)

            # Forceer UTC om foutmeldingen te voorkomen
            start_dt = start_dt.astimezone(timezone.utc)
            end_dt = end_dt.astimezone(timezone.utc)

            qs = qs.filter(
                aanvang_werkzaamheden__gte=start_dt,
                aanvang_werkzaamheden__lte=end_dt
            )

            print(f"[API] Filter toegepast van {start_dt} t/m {end_dt}")
        except Exception as e:
            print(f"[API] Fout in datumfilter: {e}")

    events = []
    for wb in qs:
        if not wb.aanvang_werkzaamheden:
            continue  # Alleen geplande werkbonnen tonen

        events.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': wb.aanvang_werkzaamheden.isoformat(),
            'resourceId': wb.behandelaar or None,
            'barcode': wb.barcode,
            'client': wb.klant.naam if wb.klant else None,
        })

        print(f"[API] → werkbon {wb.pk}: {wb.werkbonnummer} - {wb.aanvang_werkzaamheden}")

    print(f"[API] Totaal geplande werkbonnen verstuurd: {len(events)}")
    return JsonResponse(events, safe=False)

# =====================
# Werkbon handmatig verplaatsen (kalender update)
# =====================
@csrf_exempt
def werkbon_update(request, pk):
    API_ACCESS_TOKEN = "MIJNVEILIGETOKEN123"

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Alleen POST toegestaan'}, status=405)

    if request.GET.get("token") != API_ACCESS_TOKEN:
        return JsonResponse({'status': 'error', 'message': 'Ongeldige API token'}, status=403)

    try:
        werkbon = get_object_or_404(Werkbon, pk=pk)
        data = json.loads(request.body.decode('utf-8'))

        if 'start' in data:
            werkbon.aanvang_werkzaamheden = datetime.fromisoformat(data['start'].rstrip('Z'))

        if 'resourceId' in data:
            werkbon.behandelaar = data['resourceId']

        if 'status' in data:
            werkbon.status = data['status']

        werkbon.save()
        return JsonResponse({'status': 'ok'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# =====================
# Nieuwe werkbon via API aanmaken
# =====================
@csrf_exempt
def api_create_werkbon(request):
    if not is_valid_token(request):
        return JsonResponse({'error': 'Ongeldige token'}, status=403)

    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid method")

    try:
        data  = json.loads(request.body.decode('utf-8'))
        title = data.get('title')
        start = data.get('start')
        res   = data.get('resource')
        if not title or not start or not res:
            return HttpResponseBadRequest("Missing field: title, start or resource")

        dt = datetime.fromisoformat(start.rstrip('Z'))
        unique_title = f"{title}_{random.randint(1000, 9999)}"

        wb = Werkbon.objects.create(
            werkbonnummer          = unique_title,
            aanvang_werkzaamheden = dt,
            behandelaar           = res,
            status                = 'open'
        )
        return JsonResponse({'status': 'success', 'id': wb.pk})

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(str(e))

# =====================
# Werkbon ophalen op basis van barcode
# =====================

@csrf_exempt
def werkbon_op_barcode(request, barcode):
    try:
        werkbon = get_object_or_404(Werkbon, barcode=barcode)

        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode("utf-8"))
                action = data.get("action")
                if action in ["fase_afgerond", "gereed", "terug_naar_planboard"]:
                    werkbon.status = action
                    werkbon.save()
                    return JsonResponse({'success': True, 'message': f'Status bijgewerkt naar {action}'})
                else:
                    return JsonResponse({'success': False, 'message': f'Onbekende actie: {action}'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Ongeldige JSON'}, status=400)

        # GET-request voor info
        return JsonResponse({
            'id': werkbon.pk,
            'status': werkbon.status,
            'werkbonnummer': werkbon.werkbonnummer,
            'barcode': werkbon.barcode
        })

    except Werkbon.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Werkbon niet gevonden'}, status=404)

def werkbon_unscheduled(request):
    """
    Geef werkbonnen zonder aanvang_werkzaamheden (dus: terug in container).
    """
    werkbonnen = Werkbon.objects.filter(aanvang_werkzaamheden__isnull=True)
    data = [
        {
            'id': wb.pk,
            'werkbonnummer': wb.werkbonnummer,
            'klant': wb.klant.naam if wb.klant else "Geen klant"
        }
        for wb in werkbonnen
    ]
    return JsonResponse(data, safe=False)

def get_unscheduled_werkbonnen(request):
    werkbonnen = Werkbon.objects.filter(
        aanvang_werkzaamheden__isnull=True,
        status__in=['open', 'in_behandeling', 'in_lab']
    )

    data = [{
        'id': wb.id,
        'werkbonnummer': wb.werkbonnummer,
        'klant': wb.klant.naam if wb.klant else '',
    } for wb in werkbonnen]

    return JsonResponse(data, safe=False)
    
@require_POST
@csrf_exempt
def update_werkbon_status(request, werkbon_id):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Alleen POST toegestaan'}, status=405)

    try:
        werkbon = Werkbon.objects.get(pk=werkbon_id)
    except Werkbon.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Werkbon niet gevonden'}, status=404)

    try:
        data = json.loads(request.body)
        start = data.get('start')
        resource_id = data.get('resourceId')
        status = data.get('status')

        if start:
            werkbon.aanvang_werkzaamheden = make_aware(datetime.fromisoformat(start))
        if resource_id:
            werkbon.behandelaar = resource_id
        if status:
            werkbon.status = status

        werkbon.save()
        return JsonResponse({'status': 'ok'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_geplande_werkbonnen(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    qs = Werkbon.objects.filter(status__in=["open", "in_behandeling"])

    if start and end:
        try:
            start_dt = make_aware(parse_datetime(start))
            end_dt = make_aware(parse_datetime(end))
            qs = qs.filter(
                aanvang_werkzaamheden__gte=start_dt,
                aanvang_werkzaamheden__lte=end_dt
            )
        except Exception:
            pass

    qs = qs.exclude(aanvang_werkzaamheden__isnull=True)

    events = []
    for wb in qs:
        events.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': wb.aanvang_werkzaamheden.isoformat(),
            'resourceId': wb.behandelaar or None,
            'barcode': wb.barcode,
            'client': wb.klant.naam if wb.klant else None,
        })
    return JsonResponse(events, safe=False)


def get_unscheduled_werkbonnen(request):
    werkbonnen = Werkbon.objects.filter(status__in=["open", "in_behandeling"], aanvang_werkzaamheden__isnull=True)
    result = [{
        "id": wb.pk,
        "werkbonnummer": wb.werkbonnummer,
        "klant": wb.klant.naam if wb.klant else "Onbekend",
    } for wb in werkbonnen]
    return JsonResponse(result, safe=False)   
    
def print_werkbon(request, pk):
    werkbon = get_object_or_404(Werkbon, pk=pk)
    return render(request, 'planning/werkbon_print.html', {'werkbon': werkbon})    