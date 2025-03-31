import os
from pathlib import Path

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# BASE_DIR aanpassen zodat deze wijst naar de projectroot (waar manage.py staat)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'jouw-geheime-sleutel'
DEBUG = True
ALLOWED_HOSTS = []

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

INSTALLED_APPS = [
    # Django's eigen apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',  # of 'django_two_factor' afhankelijk van de package-versie

    # Eigen apps
    'apps.boekhouding',
    'apps.boekhouding.tarieven.apps.TarievenConfig',
    'apps.boekhouding.marketing.apps.MarketingConfig',
    'apps.wagenpark',
    'apps.klanten',
    'apps.klanten.klantdossier.apps.KlantdossierConfig',  # Zorg voor een aparte AppConfig voor klantdossier # ...
    'apps.hr',  # als er algemene HR-code is
    'apps.hr.werknemers.apps.WerknemersConfig',  # expliciete AppConfig voor werknemers
    'apps.planning.apps.PlanningConfig',          # expliciete AppConfig voor planning
    'apps.magazijn',
    'apps.beheerderspagina',
    'apps.log_in_pagina',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dentalmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Hiermee zoekt Django naar templates in de map "templates" op projectniveau
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'dentalmanager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'nl-NL'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
