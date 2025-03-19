from django.contrib import admin
from carritocompras.models.producto_carrito import ProductoCarrito

# Register your models here.
@admin.register(ProductoCarrito)
class ProductoCarritoAdmin(admin.ModelAdmin):
    list_display = ['producto','carrito','producto__descripcion','producto__precio','cantidad','precio_total']
    list_filter = ['carrito']
    search_fields = ['producto__nombre']