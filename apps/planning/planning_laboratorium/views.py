# Views voor planning -> planning_laboratorium

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij planning -> planning_laboratorium!')
