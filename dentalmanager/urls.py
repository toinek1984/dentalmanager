#dentalmanager/urls.py

from django.contrib import admin
from django.urls import path, include
from apps.home.views import home  # Zorg dat deze view bestaat
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin en Home
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('apps.planning.api_urls')),  # ← nieuwe file nodig
    
    # path('registration/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('registration/logout/', auth_views.LogoutView.as_view(next_page='/registration/login/'), name='logout'),
    path('registration/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'),
    path('registration/logout/', auth_views.LogoutView.as_view(next_page='/registration/login/'), name='logout'),

    # Boekhouding: dit is de algemene boekhouding-route
    path('boekhouding/', include(('apps.boekhouding.urls', 'boekhouding'), namespace='boekhouding')),
    path('planning/', include(('apps.planning.urls', 'planning'), namespace='planning')),


    # Specifieke route voor de grootboekrekeningen-submodule

    path('boekhouding/', include('apps.boekhouding.urls')),
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

