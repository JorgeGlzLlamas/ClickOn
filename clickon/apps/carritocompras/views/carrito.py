from django.views.generic import ListView
from carritocompras.models.producto_carrito import ProductoCarrito
from carritocompras.models.carrito import Carrito

class CarritoView(ListView):
    model = ProductoCarrito
    context_object_name = 'productos_carrito'
    template_name = 'carrito.html'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     return context

    def get_queryset(self):
        """
        Se filtran los productos que tiene el usuario añadidos al carrito
        """
        self.carrito = Carrito.objects.get(usuario=self.request.user)
        return ProductoCarrito.objects.filter(carrito=self.carrito)
    