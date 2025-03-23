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
    
    total_carrito = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Total del carrito', default=0.00)
    
    class Meta:
        app_label = 'carritocompras'  
        verbose_name = 'carrito'
        db_table = 'carrito_compras'
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"