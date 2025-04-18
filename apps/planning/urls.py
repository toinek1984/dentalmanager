
# apps/planning/urls.py

from django.urls import path
from . import api_views
from apps.planning.aanmaken_werkbon.views import (
    index, planboard, planboard_resource,
    edit_werkbon, create_werkbon,
    search_klant, search_opdrachtgever, print_werkbon,  werkbonnen 
)

app_name = 'planning'

urlpatterns = [
    # reguliere views
    path('', index, name='index'),
    path('planboard/', planboard, name='planboard'),
    path('planboard_resource/', planboard_resource, name='planboard_resource'),
    path('print/<int:pk>/', print_werkbon, name='werkbon_print'),
    path('create/', create_werkbon, name='create_werkbon'),
    path('edit/<int:pk>/', edit_werkbon, name='edit_werkbon'),
    path('ajax/search_klant/', search_klant, name='search_klant'),
    path('ajax/search_opdrachtgever/', search_opdrachtgever, name='search_opdrachtgever'),
    path('werkbon_overzicht/', werkbonnen, name='werkbon_overzicht'),

    # API‐routes
    path('api/resources/',          api_views.api_resources,    name='api_resources'),
    path('api/werkbonnen/',         api_views.werkbon_list,     name='api_werkbonnen'),
    path('api/werkbonnen/create/',  api_views.api_create_werkbon, name='api_werkbon_create'),
    path('api/werkbonnen/<int:pk>/update/', api_views.werkbon_update, name='api_werkbon_update'),

]

