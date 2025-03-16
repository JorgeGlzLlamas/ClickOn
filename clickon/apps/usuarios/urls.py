from django.urls import path
from .views import usuarios

app_name = 'usuarios'

urlpatterns = [
    path('inicio-sesion/', usuarios.inicio_sesion, name="sesion"),
    path('registro/', usuarios.registro, name="registro"),
    path('perfilAdmin/', usuarios.perfilAdmin, name='perfilAdmin'),
    path('perfilCliente/', usuarios.perfilCliente, name='perfilCliente'),
    path('recuperar-contrasena/', usuarios.recuperar_contrasena, name='recuperar_contrasena'),
]