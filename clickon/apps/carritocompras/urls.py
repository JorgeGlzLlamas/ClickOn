from django.urls import path
from .views import producto_carrito, carrito

app_name = 'carritocompras'

urlpatterns = [
    path('', carrito.CarritoView.as_view(), name='carrito'),
    path('vaciar-carrito/', carrito.VaciarCarritoView.as_view(), name='vaciar-carrito'),
    path('add-carrito/<int:producto>/',producto_carrito.ProductoAddCarritoView.as_view(), name='añadir-carrito'),
    path('update-carrito/<int:producto>/', producto_carrito.ProductoUpdateCarritoView.as_view(), name='actualizar-producto'),
    path('delete-carrito/<int:producto>/', producto_carrito.ProductoDeleteCarritoView.as_view(), name='eliminar-producto'),   
]