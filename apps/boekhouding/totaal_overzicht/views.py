# Views voor boekhouding -> totaal_overzicht

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij boekhouding -> totaal_overzicht!')
