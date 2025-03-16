from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from usuarios.models.usuario import Usuario
from usuarios.forms import CustomUserCreationForm

def inicio_sesion(request):
    return render(request, "inicio_sesion.html")

def registro(request):
    return render(request, "registro.html")

def perfilAdmin(request):
    return render(request, "perfilAdmin.html")

def perfilCliente(request):
    return render(request, "perfilCliente.html")

def recuperar_contrasena(request):
    return render(request, "recuperar_contrasena.html")


class RegistroView(CreateView):
    model = Usuario
    form_class = CustomUserCreationForm
    template_name = 'registro.html'  
    success_url = reverse_lazy('core:inicio')

    def form_valid(self, form):
        # Guardamos el formulario para crear el usuario
        user = form.save()
        
        # Iniciamos sesión automáticamente después del registro
        login(self.request, user)
        
        # Añadimos un mensaje de éxito más descriptivo
        messages.success(self.request, f'¡Bienvenido {user.first_name}! Tu cuenta ha sido creada exitosamente.')
        return super().form_valid(form)
        
    def form_invalid(self, form):
        # Mostramos errores específicos del formulario
        print(form.errors)  # Para depuración
        messages.error(self.request, 'Error al crear la cuenta. Por favor verifica los datos.')
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'inicio_sesion.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:inicio')
    
    def form_valid(self, form):
        messages.success(self.request, f'Bienvenido {form.get_user().get_full_name()}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos. Por favor intente nuevamente.')
        return super().form_invalid(form)
