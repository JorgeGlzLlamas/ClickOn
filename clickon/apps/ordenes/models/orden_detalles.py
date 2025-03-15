from django.db import models
from productos.models.productos import Producto
from .orden import Orden

# Modelo Productos Orden
class ProductosOrden(models.Model):

    # Orden
    orden = models.ForeignKey(
        Orden, 
        related_name='productos_orden',
        on_delete=models.CASCADE,
        verbose_name='Orden')
    
    # Producto
    producto = models.ForeignKey(
        Producto,
        related_name='productos_orden',
        on_delete=models.CASCADE,
        verbose_name='Producto')

    # Detalles del producto de la orden
    cantidad = models.IntegerField(verbose_name='Cantidad de productos de la orden')
    precio_total = models.FloatField(max_length=10, verbose_name='Precio total del producto', blank=True)
    
    class Meta:
        app_label = 'ordenes'  
        verbose_name = 'producto_orden'
        verbose_name_plural = 'producto_ordenes'
        db_table = 'producto_orden'