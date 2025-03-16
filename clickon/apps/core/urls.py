from django.urls import path
from .views import inicio

app_name = 'core'

urlpatterns = [
    path('', inicio.home, name='inicio'),
    path('establecimiento/', inicio.establecimiento, name='establecimiento'),
    path('recomendados/', inicio.recomendados, name="recomendados"),
    path('mapasitio/', inicio.mapa_sitio, name="mapasitio"),
    path('contacto/', inicio.contacto, name='contacto'),
]