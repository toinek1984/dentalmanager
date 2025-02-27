# Views voor wagenpark -> auto_2

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij wagenpark -> auto_2!')
