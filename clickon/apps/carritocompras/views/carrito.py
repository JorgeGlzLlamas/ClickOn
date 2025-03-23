from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from carritocompras.models.producto_carrito import ProductoCarrito
from carritocompras.models.carrito import Carrito
from carritocompras.forms.producto_carrito import ProductoCarritoForm
from usuarios.models.usuario import Usuario
from django.contrib.auth.mixins import LoginRequiredMixin

class CarritoView(ListView):
    model = ProductoCarrito
    context_object_name = 'productos_carrito'
    template_name = 'carrito.html'

    def get_carrito(self):
        # Obtenemos el id del usuario
        usuario = self.request.user
        self.carrito = Carrito.objects.get(usuario=usuario)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregamos el formulario por producto al contexto
        productos_con_form = []
        for producto in context['productos_carrito']:
            form = ProductoCarritoForm(instance=producto, product_id=producto.id)
            productos_con_form.append((producto, form))
        context['productos_con_form'] = productos_con_form
        context['carrito'] = self.carrito
        return context

    def get_queryset(self):
        """
        Se filtran los productos que tiene el usuario añadidos al carrito
        """
        self.carrito = Carrito.objects.get(usuario=self.request.user)
        return ProductoCarrito.objects.filter(carrito=self.carrito)


class VaciarCarritoView(View):
    def post(self, request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para añadir productos a tu carrito.")
            return redirect('/')
        
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

class DetallesCarritoView(ListView):
    model = ProductoCarrito
    context_object_name = 'productos_carrito'
    template_name = 'detalles_carrito.html'

    def get_carrito(self):
        # Obtenemos el id del usuario
        usuario = self.request.user
        self.carrito = Carrito.objects.get(usuario=usuario)

    def get_queryset(self):
        """
        Se filtran los productos que tiene el usuario añadidos al carrito
        """
        self.carrito = Carrito.objects.get(usuario=self.request.user)
        return ProductoCarrito.objects.filter(carrito=self.carrito)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carrito'] = self.carrito
        context['usuario'] = self.request.user
        return context
    
class DetallesUbicacionView(LoginRequiredMixin, DetailView):
    model = Usuario
    context_object_name = 'usuario'
    template_name = 'carrito_ubicacion.html'
    login_url = reverse_lazy('/')

    def handle_no_permission(self):
        messages.error(self.request, "Debes iniciar sesión para ver tu ubicación.")
        return redirect(self.login_url)