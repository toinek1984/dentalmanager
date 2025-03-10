from django.urls import path
from . import api_views

urlpatterns = [
    path('werkbonnen/', api_views.werkbon_list, name='api_werkbon_list'),
    path('werkbonnen/<int:pk>/update/', api_views.update_werkbon, name='api_update_werkbon'),
]
