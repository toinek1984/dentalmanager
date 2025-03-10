from pathlib import Path
import os

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# BASE_DIR aanpassen zodat deze wijst naar de projectroot (waar manage.py staat)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'jouw-geheime-sleutel'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'apps.boekhouding',
    'apps.boekhouding.tarieven.apps.TarievenConfig',
    'apps.boekhouding.marketing.apps.MarketingConfig', # Voeg dit toe
    'apps.wagenpark',
    'apps.klanten',
    'apps.hr',
    'apps.planning',
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

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

