# Views voor magazijn


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de magazijn app!')
