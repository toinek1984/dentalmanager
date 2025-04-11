from django.shortcuts import render, redirect, get_object_or_404
from .models import Crediteur
from .forms import CrediteurForm

def dashboard(request):
    items = Crediteur.objects.all()
    return render(request, 'boekhouding/crediteuren/dashboard.html', {'items': items})

def toevoegen(request):
    if request.method == 'POST':
        form = CrediteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crediteuren:dashboard')
    else:
        form = CrediteurForm()
    return render(request, 'boekhouding/crediteuren/form.html', {'form': form})

def detail(request, pk):
    item = get_object_or_404(Crediteur, pk=pk)
    return render(request, 'boekhouding/crediteuren/detail.html', {'item': item})

def bewerken(request, pk):
    item = get_object_or_404(Crediteur, pk=pk)
    if request.method == 'POST':
        form = CrediteurForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('crediteuren:dashboard')
    else:
        form = CrediteurForm(instance=item)
    return render(request, 'boekhouding/crediteuren/form.html', {'form': form})

