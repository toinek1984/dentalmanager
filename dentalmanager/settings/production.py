# Production settings
from .base import *
DEBUG = False

INSTALLED_APPS = [
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
    'apps.klanten',
    # Eigen apps
    'apps.hr.werknemers',  # ✅ Moet exact overeenkomen met jouw mappenstructuur
]