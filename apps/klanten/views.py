# Views voor klanten


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de klanten app!')
