from django.db import models
from productos.models.productos import Producto
from usuarios.models.usuario import Usuario

# Modelo Productos wishlist
class ProductoWishlist(models.Model):

    # Usuario
    usuario = models.ForeignKey(
        Usuario, 
        related_name='producto_wishlist',
        on_delete=models.CASCADE,
        verbose_name='Usuario')
    
    # Producto
    producto = models.ForeignKey(
        Producto,
        related_name='producto_wishlist',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )

    class Meta:
        app_label = 'carritocompras'  
        verbose_name = 'producto_wishlist'
        verbose_name_plural = 'productos_wishlist'
        db_table = 'producto_wishlist'