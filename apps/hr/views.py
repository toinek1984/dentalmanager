# Views voor hr
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    ...


def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij de hr app!')
