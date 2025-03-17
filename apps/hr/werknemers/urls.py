from django.urls import path
from .views import api_resources  # ✅ Zorg dat dit klopt

urlpatterns = [
    path('resources/', api_resources, name='api_resources'),
]
