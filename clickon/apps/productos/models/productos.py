from django.db import models
from establecimiento.models.establecimiento import Establecimiento
from .categoria import CategoriaProducto
from .subcategoria import SubcategoriaProducto

# Modelo de productos
class Producto(models.Model):

    # Establecimiento
    establecimiento = models.ForeignKey(
        Establecimiento, 
        related_name='producto', 
        on_delete=models.CASCADE,
        verbose_name='Establecimiento')

    # Información del establecimiento
    nombre = models.CharField(max_length=50, verbose_name="Nombre del producto")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción del producto")
    precio = models.FloatField(max_length=10, verbose_name="Precio del producto")
    imagen = models.ImageField(upload_to="img/img_productos/", verbose_name="Imagen del producto")

    # Categoría
    categoria = models.ForeignKey(
        CategoriaProducto,
        related_name='producto',
        on_delete=models.CASCADE,
        verbose_name='Categoría del producto')

    # Subcategoría
    subcategoria = models.ForeignKey(
        SubcategoriaProducto,
        related_name='producto',
        on_delete=models.CASCADE,
        verbose_name='Subcategoría del producto')

    class Meta:
        app_label = 'productos'  
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        db_table = 'producto'

    def __str__(self):
        return self.nombre