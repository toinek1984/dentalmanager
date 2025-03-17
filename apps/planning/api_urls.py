from django.urls import path
from . import api_views
from .api_views import api_resources  # Let op: import uit `api_views.p

urlpatterns = [
    path('werkbonnen/', api_views.werkbon_list, name='api_werkbon_list'),
    path('resources/', api_resources, name='api_resources'),
    path('werkbonnen/<int:pk>/update/', api_views.update_werkbon, name='api_update_werkbon'),
]
