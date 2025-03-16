from django.contrib import admin
from pagos.models.metodo_pago import MetodosPago

# Register your models here.
@admin.register(MetodosPago)
class MetodosPagoAdmin(admin.ModelAdmin):
    list_display = ['usuario','tipo_tarjeta','last_use','stripe_payment_method_id']
    list_filter = ['usuario']