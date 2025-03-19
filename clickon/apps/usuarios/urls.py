from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import autenticacion

# RegistroView, CustomLoginView, perfilAdmin, perfilCliente, recuperar_contrasena, reset_password, verificar_codigo, actualizar_contrasena

app_name = 'usuarios'

urlpatterns = [
    path('inicio-sesion/', autenticacion.CustomLoginView.as_view(), name="sesion"),
    path('registro/', autenticacion.RegistroView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='core:inicio'), name='logout'),
    path('recuperar-contrasena/', autenticacion.recuperar_contrasena, name='recuperar_contrasena'),
    path('reset-password/<uidb64>/<token>/', autenticacion.reset_password, name='reset_password'),
    path('verificar_codigo/', autenticacion.verificar_codigo, name='verificar_codigo'),
    path('actualizar_contrasena/', autenticacion.actualizar_contrasena, name='actualizar_contrasena'),
]