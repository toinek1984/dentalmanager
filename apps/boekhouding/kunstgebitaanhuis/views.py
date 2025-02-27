# Views voor boekhouding -> kunstgebitaanhuis

def index(request):
    from django.http import HttpResponse
    return HttpResponse('Welkom bij boekhouding -> kunstgebitaanhuis!')
