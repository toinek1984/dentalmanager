from django.urls import path
from . import views

urlpatterns = [
    path('', views.werkbon_overzicht, name='werkbon_overzicht'),
    path('<int:pk>/', views.werkbon_detail, name='werkbon_detail'),
    path('<int:pk>/print/', views.werkbon_print, name='werkbon_print'),
]
