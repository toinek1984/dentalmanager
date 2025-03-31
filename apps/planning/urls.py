from apps.planning.aanmaken_werkbon import views as aanmaken_views
from django.urls import path, include
from . import views

app_name = 'planning'

urlpatterns = [
    # Directe views binnen de planning-app:
    # Planboard: hoofdpagina voor de planning
    path('planboard/', views.planboard, name='planboard'),
    # Extra resource route (bijvoorbeeld voor FullCalendar resources)
    path('planboard/resource/', views.planboard_resource, name='planboard_resource'),
    
    # Werkbonnen overzicht:
    # Deze route toont het overzicht van alle werkbonnen.
    path('werkbon_overzicht/', views.werkbonnen, name='werkbon_overzicht'),
    # Detail- of printpagina voor een specifieke werkbon
    path('werkbon_overzicht/<int:pk>/print/', views.print_werkbon, name='werkbon_print'),
    
    # Route voor een lijst van werkbonnen (indien je deze apart wilt hebben)
    path('werkbonnen/', views.werkbonnen, name='werkbonnen'),
    
    # Sub-apps binnen planning:
    # Route voor aanmaken en bewerken van werkbonnen
    path('aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='aanmaken_werkbon')),
    # Route voor een apart overzicht (bijvoorbeeld extra functies voor werkbon_overzicht)
    path('overzicht/', include(('apps.planning.werkbon_overzicht.urls', 'werkbon_overzicht'), namespace='werkbon_overzicht')),
    # API routes voor de planning
    path('api/', include(('apps.planning.api_urls', 'planning_api'), namespace='planning_api')),
    
    # Extra routes voor aanvullende planboard-functies
    path('extras/', include(('apps.planning.planboard.urls', 'planboard_extras'), namespace='planboard_extras')),
]



