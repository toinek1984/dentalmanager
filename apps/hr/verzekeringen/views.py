# Views voor hr -> verzekeringen

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij hr -> verzekeringen!')
