from django.shortcuts import render

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
