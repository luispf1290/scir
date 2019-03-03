from django import forms
from insumos.models import Insumos
from django.forms import Textarea

class InsumosForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = '__all__'

        widgets = {
            'uso': Textarea(attrs={'cols':40, 'rows':6, 'Class':'form-control'}),
            'unidades' : forms.NumberInput(),
            'presentacion' : forms.NumberInput(attrs={'onkeyup' : 'mult();', 'class':'monto'})
        }

        labels = {
        	'nombre': 'Nombre',
            'empresa': 'Empresa',
        	'uso': 'Dosificacion',
        	'unidades': 'Unidades',
        	'presentacion':'Presentacion(kg, Lt)',
        	'total': 'Total'
        }