from django.urls import path
from . import views

app_name = 'kunstgebitaanhuis'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
