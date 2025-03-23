from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from carritocompras.models.carrito import Carrito
from usuarios.models.usuario import Usuario
from pagos.forms.metodo_pago import MetodoPagoForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PagarCarritoView(LoginRequiredMixin, View):
    form_class = MetodoPagoForm
    template_name = 'metodo_pago_carrito.html'
    login_url = reverse_lazy('/')

    def handle_no_permission(self):
        messages.error(self.request, "Debes iniciar sesión.")
        return redirect(self.login_url)

    def get(self, request, *args, **kwargs):
        # Se instancia el formulario vacío
        form = self.form_class()
        usuario = request.user
        carrito = get_object_or_404(Carrito, usuario=usuario)
        context = {
            'form': form,
            'usuario': usuario,
            'carrito': carrito,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Se guarda el método de pago sin comprometer la transacción a la BD aún
            metodo_pago = form.save(commit=False)
            # Asignamos el usuario actual
            metodo_pago.usuario = request.user
            metodo_pago.save()
            messages.success(request, "Método de pago agregado correctamente.")
            return redirect('/') 
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
            context = {
                'form': form,
                'usuario': request.user,
            }
            return render(request, self.template_name, context)
    