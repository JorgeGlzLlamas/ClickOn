from django.contrib import admin
from ordenes.models.orden import Orden

# Register your models here.
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['usuario']
    search_fields = ['usuario__username']