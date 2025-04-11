from django.urls import path
from . import views

app_name = 'crediteuren'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('toevoegen/', views.toevoegen, name='toevoegen'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('bewerken/<int:pk>/', views.bewerken, name='bewerken'),
]
