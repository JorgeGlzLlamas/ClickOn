from django.db import models
from django.utils import timezone
from usuarios.models.usuario import Usuario

class EstadoOrden(models.TextChoices):
    RECIBIDA = '01', 'Recibida'
    EN_ESPERA = '02', 'En esperada'
    EN_PROCESO = '03', 'En proceso'
    EN_CAMINO = '04', 'En camino'
    ENTREGADA = '05', 'Entregada'

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
    
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Fecha de Creación")

    estado_orden = models.CharField(max_length=2, choices=EstadoOrden, default=EstadoOrden.RECIBIDA)

    class Meta:
        app_label = 'ordenes'  
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'
        db_table = 'orden'