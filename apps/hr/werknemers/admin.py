from django.contrib import admin
from .models import Werknemer  # Importeer het model

@admin.register(Werknemer)
class WerknemerAdmin(admin.ModelAdmin):
    list_display = ('voornaam', 'achternaam', 'functie', 'uurloon', 'actief')
    list_filter = ('actief', 'functie')
    search_fields = ('voornaam', 'achternaam')

