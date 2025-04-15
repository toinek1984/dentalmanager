from django.urls import path, include
from . import api_views
from apps.planning.aanmaken_werkbon.views import (
    edit_werkbon, 
    index, 
    planboard, 
    planboard_resource, 
    werkbonnen, 
    print_werkbon,
    create_werkbon, 
    update_workbon, 
    search_klant, 
    search_opdrachtgever
)

app_name = 'planning'

urlpatterns = [
    # Algemene planning views
    path('', index, name='index'),
    path('planboard/', planboard, name='planboard'),
    path('planboard_resource/', planboard_resource, name='planboard_resource'),
    path('werkbon_overzicht/', werkbonnen, name='werkbon_overzicht'),
    path('print/<int:pk>/', print_werkbon, name='werkbon_print'),
    path('create/', create_werkbon, name='create_werkbon'),
    path('edit/<int:pk>/', edit_werkbon, name='edit_werkbon'),
    # Update werkbon via reguliere view (voor interne updates, niet API)
    path('update_workbon/', update_workbon, name='update_workbon'),

    # API endpoints voor werkbonnen (API-communicatie, bijvoorbeeld met Postman of mobile-app)
    path('api/werkbonnen/', api_views.api_werkbonnen, name='api_werkbonnen'),
    path('api/werkbonnen/create/', api_views.create_werkbon, name='create_werkbon'),
    path('api/werkbonnen/<int:werkbon_id>/update/', api_views.update_werkbon, name='update_werkbon'),
    path('api/resources/', api_views.api_resources, name='api_resources'),

    # AJAX zoekroutes
    path('ajax/search_klant/', search_klant, name='search_klant'),
    path('ajax/search_opdrachtgever/', search_opdrachtgever, name='search_opdrachtgever'),
]




