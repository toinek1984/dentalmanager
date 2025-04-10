from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Grootboekrekening


def dashboard(request):
    """
    Laat alle grootboekrekeningen zien in het dashboard.
    """
    rekeningen = Grootboekrekening.objects.all()
    context = {'rekeningen': rekeningen}
    return render(request, 'boekhouding/grootboekrekeningen/dashboard.html', context)


def index(request):
    return render(request, 'boekhouding/grootboekrekeningen/index.html')


def detail(request, pk):
    rekening = get_object_or_404(Grootboekrekening, pk=pk)
    return render(request, 'boekhouding/grootboekrekeningen/detail.html', {'rekening': rekening})


class GrootboekrekeningCreateView(CreateView):
    model = Grootboekrekening
    fields = ['code', 'naam', 'omschrijving']
    template_name = 'boekhouding/grootboekrekeningen/form.html'
    success_url = reverse_lazy('grootboekrekeningen:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rekening'] = None
        return context


class GrootboekrekeningUpdateView(UpdateView):
    model = Grootboekrekening
    fields = ['code', 'naam', 'omschrijving']
    template_name = 'boekhouding/grootboekrekeningen/form.html'
    success_url = reverse_lazy('grootboekrekeningen:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rekening'] = self.object
        return context
