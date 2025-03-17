from django.contrib import admin
from django.urls import path, include
from apps.home.views import home  # pas aan als je de home-view in een andere app hebt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('boekhouding/', include('apps.boekhouding.urls')),
    path('wagenpark/', include('apps.wagenpark.urls')),
    path('klanten/', include('apps.klanten.urls')),
    path('hr/', include('apps.hr.urls')),
    path('planning/', include('apps.planning.urls')),
    path('planning/aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='planning')),
    path('magazijn/', include('apps.magazijn.urls')),
    path('beheerders/', include('apps.beheerderspagina.urls')),
    path('login/', include('apps.log_in_pagina.urls')),
    path('klantdossier/', include('apps.klanten.urls')),

]
