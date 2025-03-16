from django.contrib import admin
from establecimiento.models.horario import Horario

# Register your models here.
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['establecimiento','dia','hora_apertura','hora_cierre']
    list_filter = ['establecimiento','dia']
    search_fields = ['establecimiento__nombre']
