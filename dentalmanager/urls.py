from django.contrib import admin
from django.urls import path, include
from apps.home.views import home  # Zorg dat deze view bestaat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('boekhouding/', include('apps.boekhouding.urls')),
    path('wagenpark/', include('apps.wagenpark.urls')),
    path('klanten/', include('apps.klanten.urls')),
    path('hr/', include('apps.hr.urls')),
    # Zorg dat apps/planning/urls.py bovenaan een app_name heeft
    path('planning/', include('apps.planning.urls', namespace='planning')),
    # Voor de sub-app aanmaken_werkbon, gebruik een andere namespace:
    path('planning/aanmaken/', include(('apps.planning.aanmaken_werkbon.urls', 'aanmaken_werkbon'), namespace='aanmaken_werkbon')),
    path('magazijn/', include('apps.magazijn.urls')),
    path('beheerders/', include('apps.beheerderspagina.urls')),
    path('login/', include('apps.log_in_pagina.urls')),
    path('klantdossier/', include(('apps.klanten.klantdossier.urls', 'klantdossier'), namespace='klantdossier')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)