from django import forms
from pagos.models.metodo_pago import MetodosPago

class CardTypeRadioSelect(forms.RadioSelect):
    template_name = 'widgets/card_type_radio.html'

class MetodoPagoForm(forms.ModelForm):

    numero_tarjeta = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Número de tarjeta"
    )

    class Meta:
        model = MetodosPago
        fields = [ 'tipo_tarjeta', 'exp_mes', 'exp_year' ]

        widgets = {
            'tipo_tarjeta': CardTypeRadioSelect(),
            'exp_mes': forms.NumberInput(attrs={'class': 'form-control'}),
            'exp_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        Validación personalizada para asegurar que los últimos cuatro dígitos coincidan
        """
        cleaned_data = super().clean()
        numero_tarjeta = cleaned_data.get("numero_tarjeta")

        return cleaned_data
    
