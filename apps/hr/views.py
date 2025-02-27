# Views voor hr


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de hr app!')
