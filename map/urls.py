from django.urls import path
from .views import map_view, our_view

urlpatterns = [
    path('map/', map_view, name='map'),
    path('our/', our_view, name='our'),
]