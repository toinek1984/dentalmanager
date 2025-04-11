from django.urls import path
from . import views
from .views import nza_index, nza_add  # Zorg ervoor dat nza_add hier geïmporteerd wordt

app_name = 'tarieven'  # Namespace voor deze app


urlpatterns = [
    path('', views.nza_index, name='nza_index'),
    path('add/', views.nza_add, name='nza_add'),
    path('edit/<int:pk>/', views.nza_edit, name='nza_edit'),
    path('add/', nza_add, name='nza_add'),  # Dit patroon zorgt dat '{% url 'tarieven:nza_add' %}' werkt.
]
  

