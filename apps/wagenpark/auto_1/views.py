# Views voor wagenpark -> auto_1

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij wagenpark -> auto_1!')
