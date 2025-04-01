from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, ExpressionWrapper, DecimalField, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.planning.models import Werkbon
from .models import MarketingCampagne, Provincie
from .forms import MarketingCampagneForm

def marketing_history(request):
    today = timezone.now().date()
    # Campagnes die afgelopen zijn of handmatig gearchiveerd
    campagnes = MarketingCampagne.objects.filter(
        Q(einddatum__isnull=False, einddatum__lt=today) | Q(archived=True)
    )
    # Filters ophalen uit GET-parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')
    strategie = request.GET.get('strategie')
    provincie = request.GET.get('provincie')
    if start_date:
        campagnes = campagnes.filter(startdatum__gte=start_date)
    if end_date:
        campagnes = campagnes.filter(einddatum__lte=end_date)
    if min_budget:
        campagnes = campagnes.filter(budget__gte=min_budget)
    if max_budget:
        campagnes = campagnes.filter(budget__lte=max_budget)
    if strategie:
        campagnes = campagnes.filter(strategie=strategie)
    if provincie:
        campagnes = campagnes.filter(provincie__naam=provincie)
    
    provinces = Provincie.objects.all()
    context = {
        'campaigns': campagnes,
        'filters': {
            'start_date': start_date,
            'end_date': end_date,
            'min_budget': min_budget,
            'max_budget': max_budget,
            'strategie': strategie,
            'provincie': provincie,
        },
        'provinces': provinces,
    }
    return render(request, 'boekhouding/marketing/history.html', context)

def marketing_index(request):
    campagnes = MarketingCampagne.objects.filter(actief=True, archived=False)
    return render(request, 'boekhouding/marketing/index.html', {'campagnes': campagnes})

def marketing_add(request):
    if request.method == 'POST':
        form = MarketingCampagneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marketing:marketing_index')
    else:
        form = MarketingCampagneForm()
    return render(request, 'boekhouding/marketing/add.html', {'form': form})

def marketing_dashboard(request):
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    werkbon_data = Werkbon.objects.filter(
        aanmaakdatum__gte=start_week,
        aanmaakdatum__lte=end_week,
        marketing_optie__isnull=False
    ).values(
        'marketing_optie__naam',
        'marketing_optie__provincie__naam'
    ).annotate(
        totaal_verkoop=Sum('verkoopwaarde'),
        totaal_inkoop=Sum('inkoopwaarde'),
        winst=ExpressionWrapper(Sum('verkoopwaarde') - Sum('inkoopwaarde'),
                                output_field=DecimalField(max_digits=12, decimal_places=2)),
        aantal_werkbonnen=Count('id'),
        aantal_klanten=Count('klant', distinct=True)
    )
    context = {
        'start_week': start_week,
        'end_week': end_week,
        'werkbon_data': werkbon_data,
    }
    return render(request, 'boekhouding/marketing/dashboard.html', context)

