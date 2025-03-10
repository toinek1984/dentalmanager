import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
from apps.planning.models import Werkbon
from datetime import datetime
from django.http import JsonResponse
from apps.planning.models import Werkbon

def werkbon_list(request):
    # Stel hier eventueel filters in, bijvoorbeeld:
    werkbonnen = Werkbon.objects.all()
    data = []
    for wb in werkbonnen:
        data.append({
            'id': wb.pk,
            'title': wb.werkbonnummer,
            'start': wb.aanvang_werkzaamheden.isoformat() if wb.aanvang_werkzaamheden else None,
            # Zorg ervoor dat resourceId overeenkomt met een resource in de template:
            'resourceId': wb.behandelaar,  # Of wb.technicus, afhankelijk van hoe je dat hebt ingesteld
            'status': wb.status,
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def update_werkbon(request, pk):
    if request.method == "POST":
        wb = get_object_or_404(Werkbon, pk=pk)
        try:
            data = json.loads(request.body)
            new_date_str = data.get('start')
            if new_date_str:
                # Split de string op "T" en gebruik alleen het datumgedeelte
                new_date_str = new_date_str.split("T")[0]
                new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
                wb.aanvang_werkzaamheden = new_date
                wb.save()
                return JsonResponse({'success': True})
            else:
                return HttpResponseBadRequest("Missing 'start' field.")
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid method.")