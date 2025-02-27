# Views voor klanten -> klantdossier

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij klanten -> klantdossier!')
