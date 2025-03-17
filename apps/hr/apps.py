from django.apps import AppConfig

class HrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hr'  # ✅ Zorg dat deze naam klopt met INSTALLED_APPS
