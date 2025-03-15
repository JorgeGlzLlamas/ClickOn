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
    
    total_orden = models.FloatField(max_length=10, verbose_name='Precio total de la orden')
    
    class Meta:
        app_label = 'ordenes'  
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'
        db_table = 'orden'