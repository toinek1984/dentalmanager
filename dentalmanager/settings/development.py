# Development settings
from .base import *  # ✅ Dit zorgt ervoor dat alle basisinstellingen worden geladen
import os
DEBUG = True

# Installed apps: Django apps, derde-partij apps en eigen apps
INSTALLED_APPS = [
    # Django eigen apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Derde-partij apps
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',  # Of 'django_two_factor', afhankelijk van de package-versie

    # Eigen apps (project-specifiek)
    # Indien je een algemene boekhouding-app niet gebruikt (en enkel de submodules via de AppConfigs),
    # kun je de algemene 'apps.boekhouding' eventueel weglaten.
    'apps.boekhouding.tarieven.apps.TarievenConfig',
    'apps.boekhouding.marketing.apps.MarketingConfig',
    'apps.boekhouding.grootboekrekeningen.apps.GrootboekrekeningenConfig',
    'apps.boekhouding.laboratorium',
    'apps.boekhouding.kunstgebitaanhuis',
    'apps.boekhouding.totaal_overzicht',

    'apps.wagenpark',
    'apps.klanten',
    'apps.klanten.klantdossier.apps.KlantdossierConfig',
    'apps.hr',
    'apps.hr.werknemers.apps.WerknemersConfig',
    'apps.planning.apps.PlanningConfig',
    'apps.magazijn',
    'apps.beheerderspagina',
    'apps.log_in_pagina',
]