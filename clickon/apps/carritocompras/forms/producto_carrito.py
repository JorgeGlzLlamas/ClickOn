from django import forms
from carritocompras.models.producto_carrito import ProductoCarrito

class ProductoCarritoForm(forms.ModelForm):

    cantidad = forms.IntegerField(
            min_value=1, 
            max_value=10, 
            widget=forms.NumberInput(attrs={'class': 'form-control cantidad-input'})
        )

    class Meta:
        model = ProductoCarrito
        fields = ['cantidad']
    
    def __init__(self, *args, **kwargs):
        # Se espera que se pase 'product_id' al instanciar el formulario
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        # Si se proporcionó un product_id, se actualiza el atributo 'id' del widget
        if product_id is not None:
            self.fields['cantidad'].widget.attrs.update({'id': f'cantidad-{product_id}'})
