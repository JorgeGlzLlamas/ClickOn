from django.db import models
from usuarios.models.usuario import Usuario
from .productos import Producto

# Modelo de valoración del producto
class ValoracionProducto(models.Model):

    # Producto
    producto = models.ForeignKey(
        Producto,
        related_name='valoracion',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )

    # Usuario
    usuario = models.ForeignKey(
        Usuario,
        related_name='valoracion',
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )

    # Valoración del producto (valores del 1 al 5)
    valoracion = models.CharField(max_length=1, verbose_name='Valoración del producto')

    class Meta:
        app_label = 'productos'  
        verbose_name = 'valoracion'
        verbose_name_plural = 'valoraciones'
        db_table = 'valoracion_producto'