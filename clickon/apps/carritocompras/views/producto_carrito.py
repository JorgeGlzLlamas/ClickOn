from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from productos.models.productos import Producto
from carritocompras.models.producto_carrito import ProductoCarrito
from carritocompras.models.carrito import Carrito
from usuarios.models.usuario import Usuario

class ProductoAddCarritoView(View):
    
    def dispatch(self, request, *args, **kwargs):
        
        # Obtener el id del producto de la URL
        producto_id = kwargs.get('producto')
        
        # Verificar que el producto existe
        self.producto = get_object_or_404(Producto, id=producto_id)
        
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return JsonResponse(
                {'mensaje': 'No estás autenticado. Inicia sesión para añadir productos al carrito.'}, 
                status=403)
        
        self.usuario = request.user
        self.carrito = get_object_or_404(Carrito, usuario=self.usuario.id)

        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        
        # Crear o actualizar el registro en el carrito
        producto_carrito, created = ProductoCarrito.objects.get_or_create(
            producto=self.producto,
            carrito=self.carrito,
        )
        
        # Si el producto ya estaba en el carrito, incrementa la cantidad
        if not created:
            producto_carrito.cantidad += 1
            producto_carrito.save()
        
        producto_carrito.precio_total = self.producto.precio * producto_carrito.cantidad
        producto_carrito.save()

        # Retornar un mensaje de éxito
        messages.success(request, f"¡El producto {self.producto.nombre} ha sido añadido a tu carrito!")

        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)
    

class ProductoUpdateCarritoView(View): 

    def dispatch(self, request, *args, **kwargs):
        # Obtener el id del producto de la URL
        producto_carrito_id = kwargs.get('producto')
        
        # Verificar que el producto existe en el carrito
        self.producto_carrito = get_object_or_404(ProductoCarrito, id=producto_carrito_id)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        cantidad = request.POST.get("cantidad")

        if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
            return JsonResponse({'mensaje': 'Cantidad inválida. Debe ser un número mayor a 0.'}, status=400)

        cantidad = int(cantidad)

        self.producto_carrito.precio_total = self.producto_carrito.producto.precio * cantidad
        self.producto_carrito.cantidad = cantidad
        self.producto_carrito.save() 

        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)
        