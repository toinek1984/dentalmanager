from django.shortcuts import render, redirect
from django.db.models import Sum, ExpressionWrapper, DecimalField, Count
from django.utils import timezone
from datetime import timedelta
from apps.planning.models import Werkbon
from .marketing.models import MarketingCampagne
from .marketing.forms import MarketingCampagneForm

# Algemene dashboard voor de boekhouding module
def dashboard(request):
    # Hier kun je algemene boekhoudingstatistieken toevoegen
    return render(request, 'boekhouding/dashboard.html')

# Marketing gerelateerde views

def marketing_index(request):
    # Toon actieve campagnes die niet gearchiveerd zijn
    campagnes = MarketingCampagne.objects.filter(actief=True, archived=False)
    return render(request, 'boekhouding/marketing/index.html', {'campagnes': campagnes})

def marketing_add(request):
    if request.method == 'POST':
        form = MarketingCampagneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marketing_index')
    else:
        form = MarketingCampagneForm()
    return render(request, 'boekhouding/marketing/add.html', {'form': form})

def marketing_dashboard(request):
    # Bepaal de huidige week (maandag tot zondag)
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)

    # Haal werkbonnen op binnen deze week met een gekoppelde marketingcampagne
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
        winst=ExpressionWrapper(
            Sum('verkoopwaarde') - Sum('inkoopwaarde'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ),
        aantal_werkbonnen=Count('id'),
        aantal_klanten=Count('klant', distinct=True)
    )

    context = {
        'start_week': start_week,
        'end_week': end_week,
        'werkbon_data': werkbon_data,
    }
    return render(request, 'boekhouding/marketing/dashboard.html', context)
