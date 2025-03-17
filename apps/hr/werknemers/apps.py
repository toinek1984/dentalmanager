from django.apps import AppConfig

class WerknemersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hr.werknemers'  # ✅ Moet exact overeenkomen met INSTALLED_APPS

