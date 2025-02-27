# Views voor hr -> belastingdienst

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij hr -> belastingdienst!')
