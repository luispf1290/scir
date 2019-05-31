# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core import serializers

from django.views.generic.edit import (
		CreateView,
		UpdateView,
		DeleteView,
	)
from django.views.generic import ListView

from manto.models import Mantenimiento
from manto.forms import MantenimientoForm

# Create your views here

class MantenimientoCreateView(CreateView):
    model = Mantenimiento
    template_name = "manto/mantoNew.html"
    form_class = MantenimientoForm
    success_url = reverse_lazy("manto:listManto")

    def get_context_data(self, **kwargs):
        context = super(MantenimientoCreateView, self).get_context_data(**kwargs)
        if 'formManto' not in context:
            context["formManto"] = self.form_class(self.request.GET) 
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        formManto = self.form_class(request.POST)
        if formManto.is_valid():
            manto = formManto.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=formManto))

class MantenimientoListView(ListView):
    model = Mantenimiento
    template_name = "manto/mantoList.html"

class MantenimientoUpdateView(UpdateView):
    model = Mantenimiento
    template_name = "manto/mantoNew.html"
    form_class = MantenimientoForm
    success_url = reverse_lazy('manto:listManto')

class MantenimientoDeleteView(DeleteView):
    model = Mantenimiento
    template_name = "manto/mantoDelete.html"
    success_url = reverse_lazy('manto:listManto')



def MantenimientoRealizadoUpdate(request, pk):
    #mantenimiento = Mantenimiento.objects.get(id=id_manto)
    manto = get_object_or_404(Mantenimiento, pk=pk)
    manto.aplicado=True
    manto.save(update_fields=["aplicado"])
    return HttpResponseRedirect(reverse_lazy("manto:listManto"))

def fechaManto(request):
    if request.is_ajax:
        fecha = request.GET.get('fecha')
        manto = Mantenimiento.objects.filter(fecha=fecha)
        data = serializers.serialize('json', manto, fields={'fecha','aplicado', 'descripcion'})
    else:
        data='fail'
    return HttpResponse(data, content_type='application/json')