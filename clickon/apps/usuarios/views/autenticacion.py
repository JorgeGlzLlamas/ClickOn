from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator  
from usuarios.models.usuario import Usuario
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.db import IntegrityError
from usuarios.forms.autenticacion import CustomUserCreationForm

def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Usuario.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse_lazy('usuarios:reset_password', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Enviar correo electrónico de restablecimiento de contraseña
            send_mail(
                'Recuperación de Contraseña',
                f'Haz clic en el siguiente enlace para cambiar tu contraseña: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Se ha enviado un enlace para cambiar tu contraseña a tu correo electrónico.')
            return redirect('usuarios:recuperar_contrasena')
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo electrónico no está registrado.')
            return redirect('usuarios:recuperar_contrasena')
    return render(request, 'recuperar_contrasena.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('usuarios:sesion')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        return render(request, 'reset_password.html', {'validlink': True})
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido.')
        return render(request, 'reset_password.html', {'validlink': False})

def verificar_codigo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = request.POST.get('verification_code')
        try:
            user = Usuario.objects.get(email=email, recovery_code=verification_code)
            user.recovery_code = None  # Invalidate the code after use
            user.save()
            messages.success(request, 'Código verificado correctamente. Ingresa tu nueva contraseña.')
            return redirect('usuarios:recuperar_contrasena')  # Redirect to the same page
        except Usuario.DoesNotExist:
            messages.error(request, 'Código de verificación incorrecto.')
    return render(request, 'recuperar_contrasena.html')

def actualizar_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            try:
                user = Usuario.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('usuarios:sesion')
            except Usuario.DoesNotExist:
                messages.error(request, 'Error al actualizar la contraseña.')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    return render(request, 'recuperar_contrasena.html')


class RegistroView(CreateView):
    model = Usuario
    form_class = CustomUserCreationForm
    template_name = 'registro.html'  
    success_url = reverse_lazy('usuarios:sesion')  # Changed to redirect to login page

    def form_valid(self, form):
        try:
            # Check if email already exists
            email = form.cleaned_data.get('email')
            if Usuario.objects.filter(email=email).exists():
                messages.error(self.request, f'El correo electrónico {email} ya está registrado. Por favor utiliza otro correo.')
                return self.form_invalid(form)
            
            # Redirigimos a la página de inicio de sesión (esto ya está configurado con success_url)
            return super().form_valid(form)
        
        except IntegrityError as e:
            # Capturamos errores de integridad (duplicados)
            if 'email' in str(e).lower():
                messages.error(self.request, f'Ya existe un usuario con este correo electrónico.')
            else:
                messages.error(self.request, f'Ya existe un usuario con este nombre de usuario o correo electrónico.')
            return self.form_invalid(form)
        except Exception as e:
            # Capturamos cualquier otro error
            messages.error(self.request, f'Error al crear la cuenta: {str(e)}')
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        # Mostramos errores específicos del formulario
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Error en {field}: {error}')
        
        # Si no hay errores específicos, mostramos un mensaje genérico
        if not form.errors:
            messages.error(self.request, 'No se pudo completar el registro. Por favor, revise los datos ingresados.')
        
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
