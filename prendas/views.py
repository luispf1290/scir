# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy


from django.views.generic.edit import (
		CreateView,
		UpdateView,
		DeleteView
	)

from django.views.generic import ListView


## importacion de modelos
from prendas.models import Prendas

## importacion de formularios

from prendas.forms import PrendasForm
# Create your views here.

class PrendasCreateView(CreateView):
    model = Prendas
    template_name = "prendas/newPrenda.html"
    form_class = PrendasForm
    success_url = reverse_lazy('prendas:listPrenda')

    def get_context_data(self, **kwargs):
        context = super(PrendasCreateView, self).get_context_data(**kwargs)
        if 'form2' not in context:
        	context['form2'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
    	self.object = self.get_object
    	form2 = self.form_class(request.POST)
    	if form2.is_valid():
    		prenda = form2.save()
    		return HttpResponseRedirect(self.get_success_url())
    	else:
    		return self.render_to_response(self.get_context_data(form=form2))

class PrendasListView(ListView):
    model = Prendas
    template_name = "prendas/listPrenda.html"

class PrendasUpdateView(UpdateView):
    model = Prendas
    template_name = "prendas/newPrenda.html"
    form_class = PrendasForm
    success_url = reverse_lazy('prendas:listPrenda')

class PrendasDeleteView(DeleteView):
    model = Prendas
    template_name = "prendas/deletePrenda.html"
    success_url = reverse_lazy('prendas:listPrenda')