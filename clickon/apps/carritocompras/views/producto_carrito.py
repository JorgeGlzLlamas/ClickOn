from django.views.generic import UpdateView
from django.views import View
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from productos.models.productos import Producto
from carritocompras.models.producto_carrito import ProductoCarrito
from carritocompras.models.carrito import Carrito
from carritocompras.forms.producto_carrito import ProductoCarritoForm


class ProductoAddCarritoView(View):
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir productos a tu carrito.")
            return redirect('/')
        
        # Obtener los id de los parámetros
        self.usuario = request.user
        producto_id = kwargs.get('producto')
        
        # Verificar que los objetos existen
        self.carrito = get_object_or_404(Carrito, usuario=self.usuario.id)
        self.producto = get_object_or_404(Producto, id=producto_id)

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
        
        # Calcula el precio total del producto
        producto_carrito.precio_total = self.producto.precio * producto_carrito.cantidad
        producto_carrito.save()


        # Inicializar el total del carrito en 0
        self.carrito.total_carrito = Decimal(0.00)

        # Recalcular el total del carrito a partir de los productos del carrito
        for producto in self.carrito.productos_carritos.all():
            print(f"Precio del producto: {producto.precio_total}") 
            self.carrito.total_carrito += producto.precio_total
        self.carrito.total_carrito += Decimal('50.00')
        self.carrito.save()

        # Retornar un mensaje de éxito
        messages.success(request, f"¡El producto {self.producto.nombre} ha sido añadido a tu carrito!")

        next_url = request.META.get('HTTP_REFERER', '/')
        return redirect(next_url)
    

class ProductoUpdateCarritoView(UpdateView):
    model = ProductoCarrito
    form_class = ProductoCarritoForm

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir productos a tu carrito.")
            return redirect('/')
        
        # Obtener el carrito del usuario
        carrito_id = self.kwargs.get('carrito')
        self.carrito = get_object_or_404(Carrito, id=carrito_id)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        producto_carrito_id = self.kwargs.get('producto')
        return get_object_or_404(ProductoCarrito, id=producto_carrito_id)

    def form_valid(self, form):
        # Procesa el formulario cuando es válido.
        cantidad = form.cleaned_data.get('cantidad')

        # Actualizamos la cantidad y el precio total del producto
        self.object = form.save(commit=False)
        self.object.cantidad = cantidad
        self.object.precio_total = self.object.producto.precio * cantidad
        self.object.save()

        # Inicializar el total del carrito en 0
        self.carrito.total_carrito = Decimal(0.00)

        # Recalcular el total del carrito a partir de los productos del carrito
        for producto in self.carrito.productos_carritos.all():
            print(f"Precio del producto: {producto.precio_total}") 
            self.carrito.total_carrito += producto.precio_total
        self.carrito.total_carrito += Decimal('50.00')
        self.carrito.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        # Manejo de errores si el formulario es inválido.
        messages.error(self.request, "Cantidad inválida. Debe ser un número entre 1 y 10.")
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        # Redirigir a la página anterior o página de inicio
        return self.request.META.get('HTTP_REFERER', '/')
    

class ProductoDeleteCarritoView(View):
    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir productos a tu carrito.")
            return redirect('/')
        
        # Obtenemos los id de los parámetros de la url
        carrito_id = self.kwargs.get('carrito')
        producto_carrito_id = self.kwargs.get('producto')

        # Obtenemos los objetos del carrito y del producto
        self.carrito = get_object_or_404(Carrito, id=carrito_id)
        self.producto = get_object_or_404(ProductoCarrito, id=producto_carrito_id)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Eliminar el producto del carrito
        self.producto.delete()

        # Inicializar el total del carrito en 0
        self.carrito.total_carrito = Decimal(0.00)

        # Recalcular el total del carrito a partir de los productos del carrito
        for producto in self.carrito.productos_carritos.all():
            print(f"Precio del producto: {producto.precio_total}") 
            self.carrito.total_carrito += producto.precio_total
        self.carrito.total_carrito += Decimal('50.00')
        self.carrito.save()

        # Retornar un mensaje de éxito
        messages.success(request, f"¡El producto {self.producto.producto.nombre} ha sido eliminado de tu carrito!")

        # Redirigir a la página anterior o página de inicio
        return redirect(request.META.get('HTTP_REFERER', '/'))