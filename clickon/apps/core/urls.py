from django.urls import path
from .views import inicio

app_name = 'core'

urlpatterns = [
    path('', inicio.home, name='inicio'),
    path('establecimiento/', inicio.establecimiento, name='establecimiento')
]