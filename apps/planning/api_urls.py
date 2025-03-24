from django.urls import path
from . import api_views

app_name = 'planning_api'  # Duidelijke namespace

urlpatterns = [
    path('werkbonnen/', api_views.werkbon_list, name='werkbon_list'),
    path('werkbonnen/<int:pk>/update/', api_views.update_werkbon, name='werkbon_update'),
    path('werkbonnen/create/', api_views.create_werkbon, name='create_werkbon'),
    path('resources/', api_views.api_resources, name='api_resources'),
]
