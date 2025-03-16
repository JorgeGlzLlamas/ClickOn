from django.urls import path
from django.contrib.auth.views import LogoutView
from .views.usuarios import RegistroView, CustomLoginView, perfilAdmin, perfilCliente, recuperar_contrasena

app_name = 'usuarios'

urlpatterns = [
    path('inicio-sesion/', CustomLoginView.as_view(), name="sesion"),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='core:inicio'), name='logout'),
    path('perfilAdmin/', perfilAdmin, name='perfilAdmin'),
    path('perfilCliente/', perfilCliente, name='perfilCliente'),
    path('recuperar-contrasena/', recuperar_contrasena, name='recuperar_contrasena'),
]