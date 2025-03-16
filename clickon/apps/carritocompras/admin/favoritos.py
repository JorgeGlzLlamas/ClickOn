from django.contrib import admin
from carritocompras.models.favoritos import ProductoFavoritos

# Register your models here.
@admin.register(ProductoFavoritos)
class ProductoFavoritosAdmin(admin.ModelAdmin):
    list_display = ['usuario','producto']
    list_filter = ['usuario','producto']
    search_fields = ['usuario__username']