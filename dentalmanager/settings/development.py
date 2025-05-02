# Development settings
from .base import *  # ✅ Dit zorgt ervoor dat alle basisinstellingen worden geladen
import os


SECRET_KEY = 'jouw-geheime-sleutel'  # Vervang dit door een echte, veilige sleutel voor productie
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.2.19', 'toine1984.pythonanywhere.com', ]
API_TOKEN = 'MIJNVEILIGETOKEN123'


# waar je LOGIN_URL e.d. zet:
LOGIN_URL = '/registration/login/'        # jouw login‑pagina
LOGIN_REDIRECT_URL = '/'                  # na login
# alle URL‑patronen (regex) die je wél anoniem wilt laten (bovenop LOGIN_URL):

# Alleen deze URL’s mogen zonder sessie bekeken worden:
LOGIN_EXEMPT_URLS = [
    # je eigen login/logout views
    r'^registration/login/?$',
    r'^registration/logout/?$',

    # Django’s admin login — de rest van /admin/ blijft beveiligd
    r'^admin/login/?$',

    # static en media
    r'^static/.*$',
    r'^media/.*$',
    r'^api/werkbon/barcode/.*$',
    r'^api/werkbon/update/.*$',

]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

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
    'apps.core',

    # Eigen apps (project-specifiek)
    # Indien je een algemene boekhouding-app niet gebruikt (en enkel de submodules via de AppConfigs),
    # kun je de algemene 'apps.boekhouding' eventueel weglaten.
    'apps.boekhouding.tarieven.apps.TarievenConfig',
    'apps.boekhouding.marketing.apps.MarketingConfig',
    'apps.boekhouding.grootboekrekeningen.apps.GrootboekrekeningenConfig',
    'apps.boekhouding.laboratorium',
    'apps.boekhouding.kunstgebitaanhuis',
    'apps.boekhouding.totaal_overzicht',
    'apps.boekhouding.crediteuren',
    'apps.boekhouding.debiteuren',
    'apps.boekhouding.facturatie',

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.LoginRequiredMiddleware',   # <- **hier** toevoegen

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]