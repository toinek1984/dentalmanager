from django.urls import path
from . import views

app_name = 'aanmaken_werkbon'

urlpatterns = [
    path('', views.create_werkbon, name='create_werkbon'),
    path('edit/<int:pk>/', views.edit_werkbon, name='edit_werkbon'),
    path('zoek_klant/', views.search_klant, name='zoek_klant'),
    path('zoek_opdrachtgever/', views.search_opdrachtgever, name='zoek_opdrachtgever'),
]
