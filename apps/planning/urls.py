# apps/planning/urls.py
from apps.planning.api_views import get_unscheduled_werkbonnen
from django.urls import path
from apps.planning import api_views
from . import views
from . import api_views
from apps.planning.aanmaken_werkbon.views import (
    index,
    planboard,
    planboard_resource,
    edit_werkbon,
    create_werkbon,
    search_klant,
    search_opdrachtgever,
    print_werkbon,
    werkbonnen,
)

app_name = 'planning'

urlpatterns = [
    # Webpagina's (HTML-views)
    path('', index, name='index'),
    path('planboard/', planboard, name='planboard'),
    path('planboard_resource/', planboard_resource, name='planboard_resource'),
    path('create/', create_werkbon, name='create_werkbon'),
    path('edit/<int:pk>/', edit_werkbon, name='edit_werkbon'),
    path('print/<int:pk>/', print_werkbon, name='werkbon_print'),
    path('werkbon_overzicht/', werkbonnen, name='werkbon_overzicht'),

    # AJAX zoekfunctionaliteit
    path('ajax/search_klant/', search_klant, name='search_klant'),
    path('ajax/search_opdrachtgever/', search_opdrachtgever, name='search_opdrachtgever'),

    # API-endpoints (voor scanner of externe communicatie)
    path('api/resources/', api_views.api_resources, name='api_resources'),
    path('api/werkbonnen/', api_views.werkbon_list, name='api_werkbonnen'),
    path('api/werkbonnen/create/', api_views.api_create_werkbon, name='api_werkbon_create'),
    path('api/werkbonnen/<int:pk>/update/', api_views.werkbon_update, name='api_werkbon_update'),
    path('api/werkbon/barcode/<str:barcode>/', api_views.werkbon_op_barcode, name='api_werkbon_op_barcode'),
    path('api/werkbonnen/unscheduled/', api_views.werkbon_unscheduled, name='werkbon_unscheduled'),
    
    path('api/werkbonnen/unscheduled/', api_views.get_unscheduled_werkbonnen, name='get_unscheduled_werkbonnen'),
    path('api/werkbonnen/<int:werkbon_id>/<str:actie>/', api_views.update_werkbon_status, name='update_werkbon_status'),
    path('api/werkbonnen/', api_views.werkbon_list, name='werkbon_list'),
    path('werkbon/<int:pk>/print/', api_views.print_werkbon, name='print_werkbon'),



  
    path('api/werkbonnen/', api_views.get_geplande_werkbonnen, name='get_geplande_werkbonnen'),


]
