from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "inicio.html")

def establecimiento(request):
    return render(request, "establecimiento.html")