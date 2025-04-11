from django.shortcuts import render, redirect, get_object_or_404
from .models import Factuur
from .forms import FactuurForm

def dashboard(request):
    items = Factuur.objects.all()
    return render(request, 'boekhouding/facturatie/dashboard.html', {'items': items})

def toevoegen(request):
    if request.method == 'POST':
        form = FactuurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facturatie:dashboard')
    else:
        form = FactuurForm()
    return render(request, 'boekhouding/facturatie/form.html', {'form': form})

def detail(request, pk):
    item = get_object_or_404(Factuur, pk=pk)
    return render(request, 'boekhouding/facturatie/detail.html', {'item': item})

def bewerken(request, pk):
    item = get_object_or_404(Factuur, pk=pk)
    if request.method == 'POST':
        form = FactuurForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('facturatie:dashboard')
    else:
        form = FactuurForm(instance=item)
    return render(request, 'boekhouding/facturatie/form.html', {'form': form})
