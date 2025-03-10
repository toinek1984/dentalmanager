from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='boekhouding_dashboard'),
    path('marketing/', include('apps.boekhouding.marketing.urls')),
    path('tarieven/', include('apps.boekhouding.tarieven.urls')),
    # Voeg hier andere routes toe
]
