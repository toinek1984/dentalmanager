# Development settings
from .base import *  # ✅ Dit zorgt ervoor dat alle basisinstellingen worden geladen
import os
DEBUG = True

INSTALLED_APPS = [
    'apps.klanten',
    'apps.planning',
    'apps.boekhouding.tarieven',  # ✅ Voeg deze toe
    'apps.boekhouding.marketing',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.hr.werknemers',
]
