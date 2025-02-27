# Views voor boekhouding -> laboratorium

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij boekhouding -> laboratorium!')
