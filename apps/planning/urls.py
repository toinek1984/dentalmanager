from django.urls import path, include
from . import views
from apps.planning.aanmaken_werkbon import views as aanmaken_views

app_name = 'planning'

urlpatterns = [
    # Directe views in de planning-app
    path('planboard/', views.planboard, name='planboard'),
    path('planboard/resource/', views.planboard_resource, name='planboard_resource'),
    path('werkbon_overzicht/<int:pk>/', views.print_werkbon, name='werkbon_print'),
    path('werkbonnen/', views.werkbonnen, name='werkbonnen'),

    # Sub-apps binnen planning
    path('aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='aanmaken_werkbon')),
    path('overzicht/', include(('apps.planning.werkbon_overzicht.urls', 'werkbon_overzicht'), namespace='werkbon_overzicht')),
    path('api/', include(('apps.planning.api_urls', 'planning_api'), namespace='planning_api')),
    
    # Extra routes voor aanvullende planboard-functies (als dat nodig is)
    path('extras/', include(('apps.planning.planboard.urls', 'planboard_extras'), namespace='planboard_extras')),
]
