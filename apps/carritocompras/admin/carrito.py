from django.contrib import admin
from carritocompras.models.carrito import Carrito

# Register your models here.
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario']
    search_fields = ['usuario__username']