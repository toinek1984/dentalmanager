from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from .models import NZACode, Werkfase
from .forms import NZACodeForm, WerkfaseForm
# apps/boekhouding/tarieven/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import NZACode
from .forms import NZACodeForm

def tarieven_index(request):
    nzacodes = NZACode.objects.all()
    return render(request, 'boekhouding/tarieven/index.html', {'nzacodes': nzacodes})

def tarieven_edit(request, pk):
    nzacode = get_object_or_404(NZACode, pk=pk)
    if request.method == 'POST':
        form = NZACodeForm(request.POST, instance=nzacode)
        if form.is_valid():
            form.save()
            return redirect('tarieven_index')
    else:
        form = NZACodeForm(instance=nzacode)
    return render(request, 'boekhouding/tarieven/edit.html', {'form': form})


def nza_index(request):
    codes = NZACode.objects.all()
    return render(request, 'boekhouding/tarieven/index.html', {'codes': codes})

def nza_add(request):
    WerkfaseFormSet = inlineformset_factory(NZACode, Werkfase, form=WerkfaseForm, extra=5, can_delete=False)
    if request.method == 'POST':
        form = NZACodeForm(request.POST)
        formset = WerkfaseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            nza = form.save()
            formset.instance = nza
            formset.save()
            # Verwijder werkfase-objecten die geen tijdsduur hebben ingevuld
            for wf in nza.werkfases.all():
                if not wf.duur:
                    wf.delete()
            return redirect('nza_index')
    else:
        form = NZACodeForm()
        formset = WerkfaseFormSet()
    return render(request, 'boekhouding/tarieven/add.html', {'form': form, 'formset': formset})

def nza_edit(request, pk):
    nza = get_object_or_404(NZACode, pk=pk)
    WerkfaseFormSet = inlineformset_factory(NZACode, Werkfase, form=WerkfaseForm, extra=0, can_delete=True)
    if request.method == 'POST':
        form = NZACodeForm(request.POST, instance=nza)
        formset = WerkfaseFormSet(request.POST, instance=nza)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # Verwijder werkfase-objecten zonder ingevulde tijdsduur
            for wf in nza.werkfases.all():
                if not wf.duur:
                    wf.delete()
            return redirect('nza_index')
    else:
        form = NZACodeForm(instance=nza)
        formset = WerkfaseFormSet(instance=nza)
    return render(request, 'boekhouding/tarieven/edit.html', {'form': form, 'formset': formset, 'nza': nza})

