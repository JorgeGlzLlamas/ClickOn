from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from carritocompras.models.producto_carrito import ProductoCarrito
from carritocompras.models.carrito import Carrito
from carritocompras.forms.producto_carrito import ProductoCarritoForm

class CarritoView(ListView):
    model = ProductoCarrito
    context_object_name = 'productos_carrito'
    template_name = 'carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el formulario por producto al contexto
        productos_con_form = []
        for producto in context['productos_carrito']:
            form = ProductoCarritoForm(instance=producto, product_id=producto.id)
            productos_con_form.append((producto, form))
        context['productos_con_form'] = productos_con_form
        return context

    def get_queryset(self):
        """
        Se filtran los productos que tiene el usuario añadidos al carrito
        """
        self.carrito = Carrito.objects.get(usuario=self.request.user)
        return ProductoCarrito.objects.filter(carrito=self.carrito)


class VaciarCarritoView(View):
    def post(self, request, *args, **kwargs):
        self.usuario = request.user
        self.carrito = get_object_or_404(Carrito, usuario=self.usuario)
        # Obtener los productos del carrito
        productos = self.carrito.productos_carritos.all()

        if productos.exists():
            productos.delete()
            messages.success(request, "¡Tu carrito ha sido vaciado!")
        else:
            messages.error(request, "¡No hay productos en tu carrito!")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    