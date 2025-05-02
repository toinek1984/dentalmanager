import os
from pathlib import Path

# BASE_DIR wijst naar de projectroot (waar manage.py staat)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Veiligheids- en redirect-instellingen
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
    r'^accounts/.*$', 
    r'^api/werkbon/barcode/.*$',
    r'^api/werkbon/update/.*$',
    # als je django.contrib.auth.urls gebruikt
]



# Static- en media-instellingen
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default auto field (voor Django 3.2+)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Installed apps: Django eigen apps, derde-partij apps en eigen apps
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
    'two_factor', 
    'apps.core',
    # Of 'django_two_factor', afhankelijk van de package-versie

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
    'apps.core', 

    'apps.wagenpark',
    'apps.klanten',
    'apps.klanten.klantdossier.apps.KlantdossierConfig',
    'apps.hr',
    'apps.hr.werknemers.apps.WerknemersConfig',
    'apps.hr.salarisadministratie',
    'apps.hr.verzekeringen',
    'apps.hr.uwv',
    'apps.hr.urenoverzicht',
    'apps.hr.belastingdienst',
    'apps.planning.apps.PlanningConfig',
    'apps.magazijn',
    'apps.beheerderspagina',
    'apps.log_in_pagina',
]

# Middleware configuratie
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dentalmanager.middleware.LoginRequiredMiddleware',
    
]

# Root URL-conf
ROOT_URLCONF = 'dentalmanager.urls'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Templates configuratie
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Hier zoekt Django naar je projecttemplates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI applicatie
WSGI_APPLICATION = 'dentalmanager.wsgi.application'

# Database configuratie (gebruik SQLite voor ontwikkeling)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Authentiekeer- en wachtwoordvalidatie
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationale instellingen
LANGUAGE_CODE = 'nl-NL'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
