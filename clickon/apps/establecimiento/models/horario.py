from django.db import models
from establecimiento.models.establecimiento import Establecimiento

# Catálogo de días de la semana
class Dia(models.TextChoices):
    LUNES = '1', 'Lunes'
    MARTES = '2', 'Martes'
    MIERCOLES = '3', 'Miercoles'
    JUEVES = '4', 'Jueves'
    VIERNES = '5', 'Viernes'
    SABADO = '6', 'Sábado'
    DOMINGO = '7', 'Domingo'

# Modelo horario
class Horario(models.Model):

    # Establecimiento
    establecimiento = models.ForeignKey(
        Establecimiento, 
        related_name='horario',
        on_delete=models.CASCADE,
        verbose_name="Establecimiento")

    # Información del horario del establecimiento
    dia = models.CharField(max_length=1, choices=Dia.choices)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()

    class Meta:
        app_label = 'establecimiento'  
        verbose_name = 'horario'
        verbose_name_plural = 'horarios'
        db_table = 'horario'
        ordering = ['dia']
    
    def __str__(self):
        return self.dia