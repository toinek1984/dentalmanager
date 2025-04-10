from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='boekhouding_dashboard'),
    path('marketing/', include('apps.boekhouding.marketing.urls')),
    path('tarieven/', include('apps.boekhouding.tarieven.urls')),
    path('grootboekrekeningen/', include('apps.boekhouding.grootboekrekeningen.urls', namespace='grootboekrekeningen')),

    # Voeg hier andere routes toe
]
    # path('grootboekrekeningen/', include('apps.boekhouding.grootboekrekeningen.urls', namespace='grootboekrekeningen')),
    # path('kunstgebitaanhuis/', include('apps.boekhouding.kunstgebitaanhuis.urls')),
    # path('laboratorium/', include('apps.boekhouding.laboratorium.urls')),
    # path('totaal_overzicht/', include('apps.boekhouding.totaal_overzicht.urls')),
