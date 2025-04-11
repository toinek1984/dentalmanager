from django.urls import path
from . import views

app_name = 'laboratorium'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]