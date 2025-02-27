# Views voor boekhouding -> grootboekrekeningen

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij boekhouding -> grootboekrekeningen!')
