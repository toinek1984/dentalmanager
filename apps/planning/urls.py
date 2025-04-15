from django.urls import path, include
from . import api_views
from apps.planning.aanmaken_werkbon.views import(
    edit_werkbon, 
    index, planboard, planboard_resource, werkbonnen, print_werkbon,
    create_werkbon, update_workbon, search_klant, search_opdrachtgever, print_werkbon    
)

app_name = 'planning'

urlpatterns = [
    path('', index, name='index'),
    path('planboard/', planboard, name='planboard'),
    path('planboard_resource/', planboard_resource, name='planboard_resource'),
    path('werkbon_overzicht/', werkbonnen, name='werkbon_overzicht'),
    path('api/resources/', api_views.api_resources, name='api_resources'),
    path('api/werkbonnen/', api_views.api_werkbonnen, name='api_werkbonnen'),
    path('print/<int:pk>/', print_werkbon, name='werkbon_print'),
    path('create/', create_werkbon, name='create_werkbon'),
    path('edit/<int:pk>/', edit_werkbon, name='edit_werkbon'),
    path('api/update_workbon/', update_workbon, name='update_workbon'),
    # AJAX zoekroutes
    path('ajax/search_klant/', search_klant, name='search_klant'),
    path('ajax/search_opdrachtgever/', search_opdrachtgever, name='search_opdrachtgever'),
]

    # Extra routes voor aanvullende planboard-functies
    # path('extras/', include(('apps.planning.planboard.urls', 'planboard_extras'), namespace='planboard_extras')),




