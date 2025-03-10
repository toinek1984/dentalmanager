# apps/planning/aanmaken_werkbon/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_werkbon, name='werkbon_create'),
]

