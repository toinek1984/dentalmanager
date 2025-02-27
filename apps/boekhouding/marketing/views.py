# Views voor boekhouding -> marketing

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij boekhouding -> marketing!')
