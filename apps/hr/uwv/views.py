# Views voor hr -> uwv

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij hr -> uwv!')
