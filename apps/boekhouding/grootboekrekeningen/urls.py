from django.urls import path
from . import views

app_name = 'grootboekrekeningen'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('nieuw/', views.GrootboekrekeningCreateView.as_view(), name='nieuw'),
    path('bewerken/<int:pk>/', views.GrootboekrekeningUpdateView.as_view(), name='bewerken'),
    path('', views.index, name='index'),
    path('form/', views.GrootboekrekeningCreateView.as_view(), name='form'),

]
