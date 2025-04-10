from django.contrib import admin
from django.urls import path, include
from apps.home.views import home  # Zorg dat deze view bestaat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin en Home
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Boekhouding: dit is de algemene boekhouding-route
    path('boekhouding/', include('apps.boekhouding.urls')),

    # Specifieke route voor de grootboekrekeningen-submodule
    path('boekhouding/grootboekrekeningen/', include('apps.boekhouding.grootboekrekeningen.urls', namespace='grootboekrekeningen')),
    
    # Andere apps
    path('wagenpark/', include('apps.wagenpark.urls')),
    path('klanten/', include('apps.klanten.urls')),
    path('hr/', include('apps.hr.urls')),
    path('planning/', include('apps.planning.urls', namespace='planning')),
    path('planning/aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='aanmaken_werkbon')),
    path('magazijn/', include('apps.magazijn.urls')),
    path('beheerders/', include('apps.beheerderspagina.urls')),
    path('login/', include('apps.log_in_pagina.urls')),
    path('klantdossier/', include(('apps.klanten.klantdossier.urls', 'klantdossier'), namespace='klantdossier')),

    # Een globale dashboard-route (optioneel)
    path('dashboard/', include('apps.boekhouding.grootboekrekeningen.urls', namespace='grootboekrekeningen')),
     path('tarieven/', include('apps.boekhouding.tarieven.urls', namespace='tarieven')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

