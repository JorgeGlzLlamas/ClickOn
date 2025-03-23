from django.db import models
from usuarios.models.usuario import Usuario

# Modelo Orden
class Orden(models.Model):

    # Usuario
    usuario = models.ForeignKey(
        Usuario, 
        related_name='orden',
        on_delete=models.CASCADE,
        verbose_name='Usuario')
    
    total_orden = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total de la orden', blank=True, null=True)
    total_carrito = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Total del carrito', blank=True, null=True)
    costo_envio = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Costo de envío', blank=True, null=True)

    class Meta:
        app_label = 'ordenes'  
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'
        db_table = 'orden'