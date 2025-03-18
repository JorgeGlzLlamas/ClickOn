from django.shortcuts import render
from django.views.generic import ListView
from establecimiento.models.establecimiento import Establecimiento

# Create your views here.
class EstablecimientoListView(ListView):
    model = Establecimiento
    context_object_name = 'establecimientos'
    template_name = 'establecimiento/list.html'

