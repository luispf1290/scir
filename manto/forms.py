from django import forms
from manto.models import Mantenimiento

class MantenimientoForm(forms.ModelForm):
    
    class Meta:
        model = Mantenimiento
        fields = ("fecha", "descripcion")

        widgets = {
            'descripcion' : forms.Textarea(attrs={
                'class':'form-control',
                'cols':40,
                'rows':6,
            }),

            'fecha': forms.DateInput(attrs={
                'class': 'form-control datepicker'
            })
        }

        labels = {
            'fecha':'Fecha del servicio',
            'descripcion':'Descripcion del Servicio'
        }