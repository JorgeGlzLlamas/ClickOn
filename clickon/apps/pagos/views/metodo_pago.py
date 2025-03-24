import stripe
from decimal import Decimal
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from carritocompras.models.carrito import Carrito
from carritocompras.models.producto_carrito import ProductoCarrito
from pagos.models.metodo_pago import MetodosPago
from ordenes.models.orden import Orden
from ordenes.models.orden_detalles import ProductosOrden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from pagos.models.metodo_pago import TipoTarjeta

stripe.api_key = settings.STRIPE_SECRET_KEY

class PagarCarritoView(LoginRequiredMixin, View):
    template_name = 'metodo_pago_carrito.html'
    login_url = reverse_lazy('usuarios:iniciar-sesion')

    def handle_no_permission(self):
        messages.error(self.request, "Debes iniciar sesión.")
        return redirect(self.login_url)

    def get(self, request, *args, **kwargs):
        usuario = request.user
        carrito = get_object_or_404(Carrito, usuario=usuario)
        metodos_pago = MetodosPago.objects.filter(usuario=usuario)

        # Verificar si el usuario tiene un stripe_customer_id
        if not usuario.stripe_customer_id:
            try:
                customer = stripe.Customer.create(email=usuario.email)
                usuario.stripe_customer_id = customer.id
                usuario.save()
            except Exception as e:
                messages.error(request, f"Error al crear el usuario en Stripe: {str(e)}")
                return redirect('carritocompras:carrito')

        # Para Stripe Elements necesitamos crear un setup intent en lugar de un payment intent
        # El setup intent es para guardar un método de pago sin cobrar
        try:
            setup_intent = stripe.SetupIntent.create(
                customer=usuario.stripe_customer_id,
                payment_method_types=['card'],
            )
            client_secret = setup_intent.client_secret
        except Exception as e:
            messages.error(request, f"Error al inicializar Stripe: {str(e)}")
            client_secret = None

        context = {
            'metodos_pago': metodos_pago,
            'setup_client_secret': client_secret,  # Para inicializar Stripe Elements
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'carrito': carrito,
            'usuario': usuario,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        usuario = request.user
        carrito = get_object_or_404(Carrito, usuario=usuario)
        productos_carrito = ProductoCarrito.objects.filter(carrito=carrito)
        total_final = carrito.total_carrito

        # Verificar si hay un setup_intent_id en caso de método nuevo
        setup_intent_id = request.POST.get("setup_intent_id")
        metodo_pago_id = request.POST.get("metodo_pago")

        # Si tenemos un setup_intent_id, recuperar el payment_method
        if setup_intent_id and metodo_pago_id == "nuevo":
            
            try:
                setup_intent = stripe.SetupIntent.retrieve(setup_intent_id)
                metodo_pago_id = setup_intent.payment_method
                
                # Obtener los detalles del método de pago para acceder a la información de la tarjeta
                payment_method = stripe.PaymentMethod.retrieve(metodo_pago_id)
                
                # Opcional: Guardar el método de pago para usos futuros
                if request.POST.get("guardar_metodo") == "true":
                    # Extraer la información de la tarjeta
                    card_info = payment_method.card
                    
                    # Determinar el tipo de tarjeta basado en la marca
                    tipo_tarjeta_mapping = {
                        'visa': TipoTarjeta.VISA,
                        'mastercard': TipoTarjeta.MASTERCARD,
                        'amex': TipoTarjeta.AMERICAN_EXPRESS,
                    }
                    
                    tipo_tarjeta = tipo_tarjeta_mapping.get(
                        card_info.brand.lower(), 
                        TipoTarjeta.OTRO 
                    )
                    
                    # Crear y guardar el nuevo método de pago
                    metodo_pago_obj = MetodosPago(
                        usuario=usuario,
                        stripe_payment_method_id=metodo_pago_id,
                        exp_mes=card_info.exp_month,
                        exp_year=card_info.exp_year,
                        ultimos_cuatro=card_info.last4,
                        tipo_tarjeta=tipo_tarjeta,
                        created_at=timezone.now(),
                        last_use=timezone.now()
                    )
                    metodo_pago_obj.save()
            except stripe.error.StripeError as e:
                messages.error(request, f"Error al procesar el método de pago: {e.user_message}")
                return redirect('carritocompras:metodo-pago')

        # Procesar el pago con el método seleccionado
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_final * 100),
                currency="mxn",
                customer=usuario.stripe_customer_id,
                payment_method=metodo_pago_id,
                confirm=True,
                return_url=request.build_absolute_uri(reverse('pagos:pagar-carrito')),
            )

            metodo_pago = MetodosPago.objects.get(stripe_payment_method_id=metodo_pago_id)
            # Si el pago fue exitoso
            if payment_intent.status == "succeeded":
                if metodo_pago:
                    metodo_pago.last_use = timezone.now()
                    metodo_pago.save()
                    messages.success(request, "Pago realizado con éxito.")
                
                orden = Orden.objects.create (
                    usuario=usuario,
                    total_orden=total_final - Decimal('50.00'),
                    total_carrito=total_final
                )
                orden.save()

                for producto in productos_carrito:
                    producto_orden = ProductosOrden.objects.create(
                        orden=orden,
                        producto=producto.producto,
                        cantidad=producto.cantidad,
                        precio_total=producto.precio_total
                    )
                    producto_orden.save()
                    producto.delete()
                
                carrito.total_carrito = Decimal('0.00')
                carrito.save()

                return redirect('ordenes:orden-detail-carrito', orden=orden.id)
                
            # Otros estados
            messages.warning(request, f"Estado del pago: {payment_intent.status}")
            return redirect('pagos:pagar-carrito')
            
        except stripe.error.StripeError as e:
            messages.error(request, f"Error al procesar el pago: {e.user_message}")
            return redirect('pagos:pagar-carrito')