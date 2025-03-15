from django.db import models

# Modelo categoría del producto
class CategoriaProducto(models.Model):

    # Nombre de la categoría
    categoria = models.CharField(max_length=50, verbose_name="Categoría del producto")

    class Meta:
        app_label = 'productos'  
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        db_table = 'categoria_producto'