from django.contrib import admin
from .models import Werknemer  # Importeer het model

@admin.register(Werknemer)
class WerknemerAdmin(admin.ModelAdmin):
    list_display = ('naam', 'functie', 'email', 'telefoonnummer')  # Velden die zichtbaar zijn in de admin
    search_fields = ('naam', 'email')  # Zoekfunctie
