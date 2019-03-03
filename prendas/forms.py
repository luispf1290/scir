from django import forms
from prendas.models import Prendas


class PrendasForm(forms.ModelForm):
    class Meta:
        model = Prendas
        fields = '__all__'

        labels = {
        	'nombre_prenda' : 'Prenda',
        	'no_prendas' : 'Stock'
        }
    