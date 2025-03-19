from django.urls import path
from .views import productos

app_name = 'productos'

urlpatterns = [
    path('', productos.ProductoListView.as_view(), name='producto-list')
]