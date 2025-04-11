from django.shortcuts import render, redirect, get_object_or_404
from .models import Debiteur
from .forms import DebiteurForm

def dashboard(request):
    items = Debiteur.objects.all()
    return render(request, 'boekhouding/debiteuren/dashboard.html', {'items': items})

def toevoegen(request):
    if request.method == 'POST':
        form = DebiteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('debiteuren:dashboard')
    else:
        form = DebiteurForm()
    return render(request, 'boekhouding/debiteuren/form.html', {'form': form})

def detail(request, pk):
    item = get_object_or_404(Debiteur, pk=pk)
    return render(request, 'boekhouding/debiteuren/detail.html', {'item': item})

def bewerken(request, pk):
    item = get_object_or_404(Debiteur, pk=pk)
    if request.method == 'POST':
        form = DebiteurForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('debiteuren:dashboard')
    else:
        form = DebiteurForm(instance=item)
    return render(request, 'boekhouding/debiteuren/form.html', {'form': form})

