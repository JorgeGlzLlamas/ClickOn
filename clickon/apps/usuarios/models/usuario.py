from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):

    class Rol(models.TextChoices):
        USUARIO = '1', 'Usuario'
        ADMINISTRADOR = '2', 'Administrador (Dueño)'
        EMPLEADO = '3', 'Empleado'
        SUPERADMINISTRADOR = '4', 'Superadministrador'
    
    class Meta:
        app_label = 'usuarios'  
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = 'users'

    # Se le agrega la ubicación dada en la sesión del usuario
    entidad_federativa = models.CharField(max_length=150, blank=True, verbose_name="Entidad federativa")
    municipio = models.CharField(max_length=100, blank=True, verbose_name="Municipio")
    cp = models.CharField(max_length=20, blank=True, verbose_name="Código postal")
    calle = models.CharField(max_length=150, blank=True, verbose_name="Calle")
    numero_exterior = models.CharField(max_length=20, blank=True, verbose_name="Num. exterior")
    numero_interior = models.CharField(max_length=10, blank=True, verbose_name="Num. Interior")

    # Nombre del avatar 
    avatar_name = models.CharField(max_length=20, blank=True, verbose_name="Nombre avatar")
    avatar_image_filename = models.CharField(max_length=100, blank=True, verbose_name="Nombre archivo avatar")
    # El siguiente campo requiere tener instalado el paquete Pillow
    #avatar_image = models.ImageField(upload_to='assets/avatars/', null=True, blank=True) 
    
    # Teléfono del usuario
    phone = models.CharField(max_length=50, blank=True, verbose_name="Teléfono")
    # Rol usuario
    rol_usuario = models.CharField(max_length=1, choices=Rol.choices, default=Rol.USUARIO)

    # Determina si la cuenta de usuario está bloqueda 
    is_blocked = models.BooleanField(default=False, verbose_name="Bloqueado")
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
