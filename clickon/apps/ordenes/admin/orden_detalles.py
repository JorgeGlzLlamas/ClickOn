from django.contrib import admin
from ordenes.models.orden_detalles import ProductosOrden

# Register your models here.
@admin.register(ProductosOrden)
class ProductosOrdenAdmin(admin.ModelAdmin):
    list_display = ['orden','producto','cantidad','precio_total']
    list_filter = ['orden']