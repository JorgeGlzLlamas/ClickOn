from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "inicio.html")

def establecimiento(request):
    return render(request, "establecimiento.html")

def recomendados(request):
    return render(request, "recomendados.html")

def inicio_sesion(request):
    return render(request, "inicio_sesion.html")

def registro(request):
    return render(request, "registro.html")

def recuperar_contrasena(request):
    return render(request, 'recuperar_contrasena.html')

def contacto(request):
    return render(request, 'contacto.html')