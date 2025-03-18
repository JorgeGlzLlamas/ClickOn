from django.urls import path
from .views import establecimiento

app_name = 'establecimiento'

urlpatterns = [
    path('', establecimiento.EstablecimientoListView.as_view(), name='establecimiento')
]