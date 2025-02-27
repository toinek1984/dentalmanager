# Views voor hr -> werknemers

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij hr -> werknemers!')
