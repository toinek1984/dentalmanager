from django.urls import path
from . import api_views
from .api_views import api_resources  # Let op: import uit `api_views.p

app_name = 'planning_api'  # Stel een duidelijke namespace in

urlpatterns = [
    path('werkbonnen/', api_views.werkbon_list, name='werkbon_list'),
    path('werkbonnen/<int:pk>/update/', api_views.update_werkbon, name='werkbon_update'),
    path('resources/', api_views.api_resources, name='resources'),
]