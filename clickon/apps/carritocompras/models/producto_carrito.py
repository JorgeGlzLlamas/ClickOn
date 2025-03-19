from django.db import models
from productos.models.productos import Producto
from .carrito import Carrito

# Modelo Productos de carrito
class ProductoCarrito(models.Model):

    # Carrito
    carrito = models.ForeignKey(
        Carrito, 
        related_name='productos_carritos',
        on_delete=models.CASCADE,
        verbose_name='Carrito')
    
    # Producto
    producto = models.ForeignKey(
        Producto,
        related_name='productos_carritos',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )

    # Detalles del producto del carrito
    cantidad = models.IntegerField(verbose_name='Cantidad de productos', default=1)
    precio_total = models.FloatField(max_length=10, verbose_name='Precio total del producto', blank=True, null=True)

    class Meta:
        app_label = 'carritocompras'  
        verbose_name = 'producto_carrito'
        verbose_name_plural = 'productos_carrito'
        db_table = 'producto_carrito'