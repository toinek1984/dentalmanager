# Views voor magazijn -> voorraad

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij magazijn -> voorraad!')
