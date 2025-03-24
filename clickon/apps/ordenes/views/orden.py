from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from carritocompras.models.carrito import Carrito
from ordenes.models.orden import Orden
from ordenes.models.orden_detalles import ProductosOrden

# Create your views here.
class OrdenCarritoPreviewView(View, LoginRequiredMixin):
    model = Orden
    context_object_name = 'orden'
    template_name = 'carrito_orden.html'
    login_url = reverse_lazy('usuarios:iniciar-sesion')

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Orden, pk=self.kwargs['orden'])
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Debes iniciar sesión.")
        return redirect(self.login_url)
    
    def get(self, request, *args, **kwargs):
        usuario = request.user
        carrito = get_object_or_404(Carrito, usuario=usuario)

        productos_orden = ProductosOrden.objects.filter(orden=self.object)

        context = {
            'usuario': usuario,
            'carrito': carrito,
            'productos_orden': productos_orden,
            'orden': self.object
        }
        return render(request, self.template_name, context)
    
