from django.contrib import admin
from carritocompras.models.wishlist import ProductoWishlist

# Register your models here.
@admin.register(ProductoWishlist)
class ProductoWishlistAdmin(admin.ModelAdmin):
    list_display = ['usuario','producto']
    list_filter = ['usuario','producto']
    search_fields = ['usuario__username']