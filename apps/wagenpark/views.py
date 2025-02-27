# Views voor wagenpark


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de wagenpark app!')
