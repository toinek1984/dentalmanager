from django.urls import path
from . import views

app_name = 'tarieven'  # Namespace voor deze app


urlpatterns = [
    path('', views.nza_index, name='nza_index'),
    path('add/', views.nza_add, name='nza_add'),
    path('edit/<int:pk>/', views.nza_edit, name='nza_edit'),
  
]
