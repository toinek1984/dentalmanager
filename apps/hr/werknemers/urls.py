from django.urls import path
  # ✅ Zorg dat dit klopt
from . import views

app_name = 'werknemers'

urlpatterns = [
    path('', views.werknemer_index, name='werknemer_index'),
    path('toevoegen/', views.werknemer_toevoegen, name='werknemer_toevoegen'),  # ✅ deze moet erin staan
    path('nieuw/', views.werknemer_add, name='add'),
    path('bewerk/<int:pk>/', views.werknemer_edit, name='edit'),
    path('detail/<int:pk>/', views.werknemer_detail, name='detail'),
]
