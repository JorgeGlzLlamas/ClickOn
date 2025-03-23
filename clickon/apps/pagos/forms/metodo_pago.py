from django import forms
from pagos.models.metodo_pago import MetodosPago

class CardTypeRadioSelect(forms.RadioSelect):
    template_name = 'widgets/card_type_radio.html'

class MetodoPagoForm(forms.ModelForm):

    class Meta:
        model = MetodosPago
        fields = [
            'tipo_tarjeta', 'ultimos_cuatro','exp_mes','exp_year'
        ]

        widgets = {
            'tipo_tarjeta': CardTypeRadioSelect(),
            'ultimos_cuatro': forms.TextInput(attrs={'class': 'form-control'}),
            'exp_mes': forms.NumberInput(attrs={'class': 'form-control'}),
            'exp_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }