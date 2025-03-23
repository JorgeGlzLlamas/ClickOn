from django.urls import path
from .views import metodo_pago

app_name = 'pagos'

urlpatterns = [
    path('carrito-pago/', metodo_pago.PagarCarritoView.as_view(), name='pagar-carrito')
]