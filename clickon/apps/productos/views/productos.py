from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from productos.models.productos import Producto

# Create your views here.
class ProductoListView(ListView):
    model = Producto
    context_object_name = 'productos'
    template_name = 'productos/producto_list.html'

    