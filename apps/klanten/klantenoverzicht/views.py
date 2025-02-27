# Views voor klanten -> klantenoverzicht

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij klanten -> klantenoverzicht!')
