from django import forms
from area.models import Area


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'

        labels = {
        	'codigo' : 'Codigo Area',
        	'nombre_area': 'Area',
        	'stock': 'Stock'
        }
    