from django.urls import path
from .views import create_werkbon, search_klant, search_opdrachtgever

app_name = 'aanmaken_werkbon'
urlpatterns = [
    # Gebruik de geïmporteerde create_werkbon-functie als de hoofdroute
    path('', create_werkbon, name='aanmaken'),
    # Als je een aparte naam wilt voor dezelfde view kun je ook een extra route toevoegen:
    # path('werkbon/', create_werkbon, name='werkbon_aanmaken'),
    path('zoek_klant/', search_klant, name='zoek_klant'),
    path('zoek_opdrachtgever/', search_opdrachtgever, name='zoek_opdrachtgever'),
]
