from django.shortcuts import render, get_object_or_404
from apps.planning.models import Werkbon

def werkbon_overzicht(request):
    werkbonnen = Werkbon.objects.all()
    return render(request, 'planning/index.html', {'werkbonnen': werkbonnen})

def werkbon_detail(request, pk):
    werkbon = get_object_or_404(Werkbon, pk=pk)
    return render(request, 'planning/detail.html', {'werkbon': werkbon})

def werkbon_print(request, pk):
    werkbon = get_object_or_404(Werkbon, pk=pk)
    return render(request, 'planning/print.html', {'werkbon': werkbon})
