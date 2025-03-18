from django.contrib import admin
from productos.models.productos import Producto

# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','categoria','subcategoria','descripcion','precio','imagen']
    list_filter = ['categoria','subcategoria']
    search_fields = ['nombre']