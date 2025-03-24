from django.urls import path
from .views import orden

app_name = 'ordenes'

urlpatterns = [
    path('carrito-orden/<int:orden>/', orden.OrdenCarritoPreviewView.as_view(), name='orden-detail-carrito')
]