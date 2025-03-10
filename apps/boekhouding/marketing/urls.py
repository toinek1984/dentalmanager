from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketing_index, name='marketing_index'),
    path('add/', views.marketing_add, name='marketing_add'),
    path('dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    path('history/', views.marketing_history, name='marketing_history'),
]
