from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy


### clases que se utilizan para un crud basico
from django.views.generic.edit import (
		CreateView,
		UpdateView,
		DeleteView
	)
from django.views.generic import ListView

#### Importacion de los modelos #####

from insumos.models import Insumos

### Importacion de los formulario #####

from insumos.forms import InsumosForm

# Create your views here.

class InsumosCreateView(CreateView):
    model = Insumos
    template_name = "insumos/newInsumos.html"
    form_class = InsumosForm
    success_url = reverse_lazy('insumos:listInsumo')

    def get_context_data(self, **kwargs):
        context = super(InsumosCreateView, self).get_context_data(**kwargs)
        if 'formInsum' not in context:
        	context['formInsum'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
    	self.object = self.get_object
    	formInsum = self.form_class(request.POST)
    	if formInsum.is_valid():
    		insumo = formInsum.save()
    		return HttpResponseRedirect(self.get_success_url())
    	else:
    		return self.render_to_response(self.get_context_data(form=formInsum))

class InsumosListView(ListView):
    model = Insumos
    template_name = "insumos/listInsumos.html"

class InsumosUpdateView(UpdateView):
    model = Insumos
    template_name = "insumos/newInsumos.html"
    form_class = InsumosForm
    success_url = reverse_lazy('insumos:listInsumo')

class InsumosDeleteView(DeleteView):
    model = Insumos
    template_name = "insumos/deleteInsumos.html"
    success_url = reverse_lazy('insumos:listInsumo')


###### funcion para  el detalle de insumos con AJAX ######

from django.core import serializers
import json

def DetailAjax(request):
    model = Insumos
    id_insumo = request.GET.get('id')
    product = model.objects.filter(id=id_insumo)
    datos = serializers.serialize('json', product, fields=('codigo', 'nombre', 'uso', 'unidades', 'presentacion', 'total'))

    return HttpResponse(datos, content_type='application/json')