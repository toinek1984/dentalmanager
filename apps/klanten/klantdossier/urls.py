from django.urls import path
from . import views



urlpatterns = [
    path('<int:klant_id>/', views.dossier_detail, name='dossier_detail'),
    path('', views.index, name='index'),
]
