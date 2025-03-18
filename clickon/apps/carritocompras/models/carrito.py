from django.db import models
from usuarios.models.usuario import Usuario

# Modelo Carrito
class Carrito(models.Model):

    # Usuario
    usuario = models.ForeignKey(
        Usuario, 
        related_name='carrito',
        on_delete=models.CASCADE,
        verbose_name='Usuario')
    
    class Meta:
        app_label = 'carritocompras'  
        verbose_name = 'carrito'
        db_table = 'carrito_compras'
    