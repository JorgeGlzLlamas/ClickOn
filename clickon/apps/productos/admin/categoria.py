from django.contrib import admin
from productos.models.categoria import CategoriaProducto

# Register your models here.
@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['categoria']