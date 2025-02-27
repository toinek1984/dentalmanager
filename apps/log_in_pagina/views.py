# Views voor log_in_pagina


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de log_in_pagina app!')
