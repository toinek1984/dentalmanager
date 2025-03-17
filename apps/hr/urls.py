from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('werknemers/', include('apps.hr.werknemers.urls')),  # ✅ Dit voegt de werknemers-API toe!
]
