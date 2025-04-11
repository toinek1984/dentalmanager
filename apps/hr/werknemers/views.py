from django.shortcuts import render, get_object_or_404, redirect
from .models import Werknemer
from .forms import WerknemerForm

def werknemer_index(request):
    werknemers = Werknemer.objects.all()
    return render(request, 'hr/werknemers/index.html', {'werknemers': werknemers})

def werknemer_detail(request, pk):
    werknemer = get_object_or_404(Werknemer, pk=pk)
    return render(request, 'hr/werknemers/detail.html', {'werknemer': werknemer})

def werknemer_add(request):
    if request.method == 'POST':
        form = WerknemerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('werknemers:index')
    else:
        form = WerknemerForm()
    return render(request, 'hr/werknemers/form.html', {'form': form})

def werknemer_edit(request, pk):
    werknemer = get_object_or_404(Werknemer, pk=pk)
    if request.method == 'POST':
        form = WerknemerForm(request.POST, instance=werknemer)
        if form.is_valid():
            form.save()
            return redirect('werknemers:index')
    else:
        form = WerknemerForm(instance=werknemer)
    return render(request, 'hr/werknemers/form.html', {'form': form, 'werknemer': werknemer})

def werknemer_toevoegen(request):
    if request.method == 'POST':
        form = WerknemerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('werknemers:werknemer_index')
    else:
        form = WerknemerForm()
    return render(request, 'hr/werknemers/form.html', {'form': form})