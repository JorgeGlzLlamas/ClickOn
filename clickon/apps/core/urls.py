from django.urls import path
from .views import inicio

app_name = 'core'

urlpatterns = [
    path('', inicio.home, name='inicio'),
    path('recomendados/', inicio.recomendados, name="recomendados"),
    path('inicio-sesion/', inicio.inicio_sesion, name="sesion"),
    path('registro/', inicio.registro, name="registro"),
    path('mapasitio/', inicio.mapa_sitio, name="mapasitio")
]