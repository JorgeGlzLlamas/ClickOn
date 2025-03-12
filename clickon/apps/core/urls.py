from django.urls import path
from .views import inicio

app_name = 'core'

urlpatterns = [
    path('', inicio.home, name='inicio'),
    path('establecimiento/', inicio.establecimiento, name='establecimiento'),
    path('recomendados/', inicio.recomendados, name="recomendados"),
    path('inicio-sesion/', inicio.inicio_sesion, name="sesion"),
    path('registro/', inicio.registro, name="registro"),
    path('recuperar-contrasena/', inicio.recuperar_contrasena, name='recuperar_contrasena'),
    path('contacto/', inicio.contacto, name='contacto')
]