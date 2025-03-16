from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('usuario/', include('apps.usuarios.urls')),
    path('establecimiento/', include('apps.establecimiento.urls')),
    path('clickon/', include('apps.productos.urls')),
    path('carrito/', include('apps.carritocompras.urls')),
    path('orden/', include('apps.ordenes.urls')),
    path('administracion/',include('apps.administracion.urls')),
    path('busquedas/', include('apps.busquedas.urls')),
    path('feedback/', include('apps.feedbacks.urls')),
    path('compra/', include('apps.pagos.urls')),
]
