# Views voor magazijn -> bestellijst

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij magazijn -> bestellijst!')
