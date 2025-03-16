from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios.models.usuario import Usuario

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol_usuario', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Ubicación usuario', {
            'fields': ('entidad_federativa', 'municipio', 'cp', 'calle', 'numero_exterior', 'numero_interior')
        }),
        ('Información adicional',{
            'fields':('phone', 'rol_usuario', 'avatar_image', 'stripe_customer_id')
        })
    )