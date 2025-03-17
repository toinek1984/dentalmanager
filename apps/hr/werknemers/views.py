from django.http import JsonResponse
from .models import Werknemer  # ✅ Zorg dat dit klopt met jouw models.py

def api_resources(request):
    """ Geeft een JSON-lijst met alle medewerkers terug voor FullCalendar. """
    werknemers = Werknemer.objects.all().values('id', 'naam')
    data = [{'id': w['id'], 'title': w['naam']} for w in werknemers]
    return JsonResponse(data, safe=False)

