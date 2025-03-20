from django.urls import path
from . import views

app_name = 'klantdossier'

urlpatterns = [
    path('<int:klant_id>/', views.dossier_detail, name='detail'),
    # Voeg hier eventueel meer URL-patronen toe (bijv. edit, create, etc.)
]
