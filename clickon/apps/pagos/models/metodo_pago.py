from django.db import models
from usuarios.models.usuario import Usuario

# Catálogo de tipos de tarjeta disponibles en la app
class TipoTarjeta(models.TextChoices):
    VISA = '01', 'VISA'
    MASTERCARD = '02', 'MASTERCARD'
    AMERICAN_EXPRESS = '03', 'AMERICAN EXPRESS'

# Modelo Métodos de pago
class MetodosPago(models.Model):

    # Usuario
    usuario = models.ForeignKey(
        Usuario, 
        related_name='metodos_pago',
        on_delete=models.CASCADE,
        verbose_name='Usuario')
    
    # ID método de pago de stripe (Proporcionado por el API de Stripe Payments)
    stripe_payment_method_id = models.CharField(max_length=100, verbose_name='ID método pago', null=True, blank=True)

    # Tipo tarjeta
    tipo_tarjeta = models.CharField(max_length=2, choices=TipoTarjeta.choices, default=TipoTarjeta.VISA, verbose_name='Tipo tarjeta')

    # Información de tarjeta
    ultimos_cuatro = models.CharField(max_length=4)
    exp_mes = models.IntegerField(verbose_name='Mes de expiración')
    exp_year = models.IntegerField(verbose_name='Año de expiración')

    # Método de pago por defecto
    is_default = models.BooleanField(default=False, verbose_name='Método de pago por defecto')

    # Método de pago (creación y último)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación del método')
    last_use = models.DateTimeField(verbose_name='Último uso de tarjeta', null=True, blank=True)
    
    class Meta:
        app_label = 'pagos'  
        verbose_name = 'metodo_pago'
        verbose_name_plural = 'metodos_pago'
        db_table = 'metodo_pago'

    def get_tarjeta_imagen(self):
        imagenes = {
            TipoTarjeta.VISA: 'img/metodo_pago/visa.webp',
            TipoTarjeta.MASTERCARD: 'img/metodo_pago/mastercard.webp',
            TipoTarjeta.AMERICAN_EXPRESS: 'img/metodo_pago/american_express.webp',
        }
        return imagenes.get(self.tipo_tarjeta, 'No hay imagen asociada')