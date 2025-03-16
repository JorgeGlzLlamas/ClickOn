from django.contrib import admin
from productos.models.valoracion import ValoracionProducto

# Register your models here.
@admin.register(ValoracionProducto)
class ValoracionProductoAdmin(admin.ModelAdmin):
    list_display = ['producto','usuario','valoracion']
    search_fields = ['producto__nombre']