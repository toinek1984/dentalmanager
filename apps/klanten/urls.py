from django.urls import path
from . import views

app_name = 'klanten'

urlpatterns = [
    path('', views.klantenoverzicht, name='klantenoverzicht'),
    path('json/', views.klanten_json, name='klanten_json'),
    
    path('dossiers/', views.dossier_list, name='dossier_list'),
    path('dossiers/nieuw/', views.dossier_create, name='dossier_create'),
    path('dossiers/<int:klantnummer>/', views.dossier_detail, name='dossier_detail'),
    path('dossiers/<int:klantnummer>/bewerken/', views.dossier_edit, name='dossier_edit'),
    path('dossiers/<int:klantnummer>/werkbon/nieuw/', views.open_werkbon_form, name='werkbon_create'),
    path('dossiers/<int:klantnummer>/overleden/', views.mark_overleden, name='mark_overleden'),
    path('dossiers/<int:klantnummer>/notities/add/', views.add_notitie, name='add_notitie'),
    
    # Als deze routes bedoeld zijn voor specifieke pagina's, zorg dan dat de bijbehorende views bestaan:
    path('klantenoverzicht/', views.klantenoverzicht, name='klantenoverzicht_page'),
    path('klantaanmaken/', views.klantaanmaken, name='klantaanmaken'),
    # Verwijder of hernoem 'klantdossier/' omdat deze conflicteert met de detailview (die een klantnummer verwacht)
]
