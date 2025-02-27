# Views voor beheerderspagina


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de beheerderspagina app!')
