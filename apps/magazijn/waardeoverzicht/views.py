# Views voor magazijn -> waardeoverzicht

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij magazijn -> waardeoverzicht!')
