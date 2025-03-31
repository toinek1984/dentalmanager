from django.urls import path
from . import views

app_name = 'klantdossier'

urlpatterns = [
    path('<int:klant_id>/', views.dossier_detail, name='dossier_detail'),
]
