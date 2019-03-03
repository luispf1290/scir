from django import forms
from solicitud.models import Solicitud, Integral
from django.forms.models import inlineformset_factory

class IntegralForm(forms.ModelForm):
	
	class Meta:
		model = Integral
		fields = ['folio', 'fk_turno', 'fk_recol', 'fk_area']
		widgets = {
			'folio' : forms.TextInput(attrs={
				'class' : 'form-control',
				'required' : True,
				'placeholder':'Folio'
			}),

			'fk_turno' : forms.Select(attrs={
				'class' : 'form-control',
				'required' : True
			}),

			'fk_recol' : forms.Select(attrs={
				'class' : 'form-control',
				'required' : True
			}),

			'fk_area' : forms.Select(attrs={
				'class':'form-control',
				'required':True
			})
		}


class SolicitudForm(forms.ModelForm):
    class Meta:
		model = Solicitud
		fields = ['recibe_serv', 'recibe_lav', 'total_serv', 'total_lav', 'fk_prenda']
		
		labels = {
			'fk_prenda':'lavabo'
		}
		
		widgets = {

			'recibe_serv':forms.NumberInput(attrs={
				'value' : '0'
			}),

			'recibe_lav':forms.NumberInput(attrs={
				'value':'0'
			}),

			'total_serv':forms.NumberInput(attrs={
				'value':'0'
			}),

			'total_lav':forms.NumberInput(attrs={
				'value':'0'
			})
		}

Integral_Solicitud_Formset = inlineformset_factory(Integral, Solicitud, form=SolicitudForm, extra=25)