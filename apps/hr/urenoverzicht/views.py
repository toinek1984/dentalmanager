# Views voor hr -> urenoverzicht

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij hr -> urenoverzicht!')
