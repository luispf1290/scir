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

####### Importacion de los modelos ####
from area.models import Area

##### importacion de los formularios ####

from area.forms import AreaForm

# Create your views here.

def menuAreas(request):
    area_colum1 = Area.objects.all().order_by('id')[:11]
    area_colum2 = Area.objects.all().order_by('id')[11:22]
    template = loader.get_template('menus/menuAreas.html')
    context = {
        'colum1':area_colum1,
        'colum2':area_colum2
    }

    return HttpResponse(template.render(context, request))

########### Clases del modelo Area ################
class AreaCreateView(CreateView):
    model = Area
    template_name = "areas/newArea.html"
    form_class = AreaForm
    success_url = reverse_lazy('area:listAreas')

    def get_context_data(self, **kwargs):
        context = super(AreaCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
        	context['form'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
    	self.object = self.get_object
    	form = self.form_class(request.POST)
    	if form.is_valid():
    	 	area = form.save()
    	 	return HttpResponseRedirect(self.get_success_url())
    	else:
    		return self.render_to_response(self.get_context_data(form=form))

class AreaListView(ListView):
    model = Area
    template_name = "areas/listArea.html"

class AreaUpdateView(UpdateView):
    model = Area
    template_name = "areas/newArea.html"
    form_class = AreaForm
    success_url = reverse_lazy('area:listAreas')

class AreaDeleteView(DeleteView):
    model = Area
    template_name = "areas/deleteArea.html"
    success_url = reverse_lazy('area:listAreas')
