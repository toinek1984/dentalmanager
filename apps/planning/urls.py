from django.urls import path, include
from . import views

urlpatterns = [
    path('planboard/', views.planboard_resource, name='planboard_resource'),
    path('planboard/', views.planboard, name='planboard'),
    path('aanmaken/', include('apps.planning.aanmaken_werkbon.urls')),
    path('overzicht/', include('apps.planning.werkbon_overzicht.urls')),
    path('planboard/', include('apps.planning.planboard.urls')),
    path('api/', include('apps.planning.api_urls')),  # Nieuwe API-endpoints
]
