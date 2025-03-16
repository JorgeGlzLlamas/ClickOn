from django.db import models
from productos.models.productos import Producto
from usuarios.models.usuario import Usuario

# Modelo Productos favoritos
class ProductoFavoritos(models.Model):

    # Usuario
    usuario = models.ForeignKey(
        Usuario, 
        related_name='producto_favorito',
        on_delete=models.CASCADE,
        verbose_name='Usuario')
    
    # Producto
    producto = models.ForeignKey(
        Producto,
        related_name='producto_favorito',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )

    class Meta:
        app_label = 'carritocompras'  
        verbose_name = 'producto_favorito'
        verbose_name_plural = 'productos_favoritos'
        db_table = 'producto_favorito'