# Views voor boekhouding


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de boekhouding app!')
