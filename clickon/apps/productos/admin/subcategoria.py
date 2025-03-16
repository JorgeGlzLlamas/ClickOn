from django.contrib import admin
from productos.models.subcategoria import SubcategoriaProducto

# Register your models here.
@admin.register(SubcategoriaProducto)
class SubcategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['categoria','subcategoria']
    list_filter = ['categoria']