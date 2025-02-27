# Views voor planning -> werkbon_overzicht

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij planning -> werkbon_overzicht!')
