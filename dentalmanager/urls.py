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
    path('boekhouding/', include(('apps.boekhouding.urls', 'boekhouding'), namespace='boekhouding')),
    path('planning/', include(('apps.planning.urls', 'planning'), namespace='planning')),


    # Specifieke route voor de grootboekrekeningen-submodule

    
    # Andere apps
    path('wagenpark/', include('apps.wagenpark.urls')),
    path('klanten/', include('apps.klanten.urls')),
    path('hr/', include('apps.hr.urls')),
    path('planning/aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='aanmaken_werkbon')),
    path('magazijn/', include('apps.magazijn.urls')),
    path('beheerders/', include('apps.beheerderspagina.urls')),
    path('login/', include('apps.log_in_pagina.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

