from django.db import models
from .categoria import CategoriaProducto

# Modelo subcategoría del producto
class SubcategoriaProducto(models.Model):

    # Categoria
    categoria = models.ForeignKey(
        CategoriaProducto,
        related_name='subcategoria',
        on_delete=models.CASCADE,
        verbose_name='Categoria'
    )

    # Nombre de la subcategoría
    subcategoria = models.CharField(max_length=50, verbose_name="Subcategoría del producto")

    class Meta:
        app_label = 'productos'  
        verbose_name = 'subcategoria'
        verbose_name_plural = 'subcategorias'
        db_table = 'subcategoria_producto'

    def __str__(self):
        return self.subcategoria