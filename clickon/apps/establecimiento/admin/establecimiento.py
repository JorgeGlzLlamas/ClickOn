from django.contrib import admin
from establecimiento.models.establecimiento import Establecimiento

# Register your models here.
@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ['usuario','nombre','logo']
