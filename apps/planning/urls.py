from django.urls import path, include
from . import views

app_name = 'planning'

urlpatterns = [
    # Directe views
    path('planboard/', views.planboard, name='planboard'),
    path('planboard/resource/', views.planboard_resource, name='planboard_resource'),
    
    # Sub-apps
    path('aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='aanmaken_werkbon')),
    path('overzicht/', include('apps.planning.werkbon_overzicht.urls')),
    path('planboard/', include('apps.planning.planboard.urls')),
    path('api/', include('apps.planning.api_urls', namespace='planning_api')),
    path('werkbonnen/', views.werkbonnen, name='werkbonnen'),
]
