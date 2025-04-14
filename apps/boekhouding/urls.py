from django.urls import path, include
from . import views

urlpatterns = [
    path('crediteuren/', include('apps.boekhouding.crediteuren.urls', namespace='crediteuren')),
    path('debiteuren/', include('apps.boekhouding.debiteuren.urls', namespace='debiteuren')),
    path('facturatie/', include('apps.boekhouding.facturatie.urls', namespace='facturatie')),
    path('dashboard/', views.dashboard, name='boekhouding_dashboard'),
    path('marketing/', include('apps.boekhouding.marketing.urls')),
    path('tarieven/', include('apps.boekhouding.tarieven.urls', namespace= 'tarieven')),
    path('grootboekrekeningen/', include('apps.boekhouding.grootboekrekeningen.urls', namespace='grootboekrekeningen')),
    path('kunstgebitaanhuis/', include('apps.boekhouding.kunstgebitaanhuis.urls')),
    path('laboratorium/', include('apps.boekhouding.laboratorium.urls')),

    # Voeg hier andere routes toe
]
    # path('grootboekrekeningen/', include('apps.boekhouding.grootboekrekeningen.urls', namespace='grootboekrekeningen')),
    # path('kunstgebitaanhuis/', include('apps.boekhouding.kunstgebitaanhuis.urls')),
    # path('laboratorium/', include('apps.boekhouding.laboratorium.urls')),
    # path('totaal_overzicht/', include('apps.boekhouding.totaal_overzicht.urls')),
