from django.db import models
from usuarios.models.usuario import Usuario

# Create your models here.
class Establecimiento(models.Model):

    # Dueño del establecimiento
    usuario = models.OneToOneField(
        Usuario, 
        related_name='establecimiento', 
        on_delete=models.CASCADE,
        verbose_name="ID usuario - dueño ")

    # Información del establecimiento
    nombre = models.CharField(max_length=50, verbose_name="Nombre del establecimiento")
    logo = models.ImageField(upload_to="img/establecimiento_logo/", verbose_name="Logo del establecimiento")
    
    # Dirección del establecimiento
    entidad = models.CharField(max_length=60, verbose_name="Entidad del establecimiento")
    municipio= models.CharField(max_length=60, verbose_name="Muncipio del establecimiento")
    codigo_postal = models.CharField(max_length=6, verbose_name="Código postal del establecimiento")
    colonia = models.CharField(max_length=50, verbose_name="Colonia del establecimiento")
    calle = models.CharField(max_length=50, verbose_name="Calle del establecimiento")
    numero_exterior = models.CharField(max_length=5, verbose_name="Num. Exterior del establecimiento")
    numero_interior = models.CharField(max_length=5, verbose_name="Num. Interior del establecimiento", blank=True, null=True)

    class Meta:
        app_label = 'establecimiento'  
        verbose_name = 'establecimiento'
        db_table = 'establecimiento'