# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core import serializers

## libresrias para el sign up
from django.contrib.auth import login, authenticate

### importacion de los formularios
from usuario.forms import UserForm 

from usuario.models import User
from manto.models import Mantenimiento

from django.views.generic import ListView


# Create your views here.

## funcion de la vista de la pagina principal(Login)
def index(request):
    
    return render(request, 'index.html')

def menuPrincipal(request):
    return render(request, 'menus/menuPrincipal.html')

def signUp(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('first')
    else :
        form = UserForm()
    return render(request, 'Usuarios/newUsuario.html',{'form' :form})

class UserListView(ListView):
    model = User
    template_name = "Usuarios/listUsuario.html"

def fechaManto(request):
    if request.is_ajax:
        fecha = request.GET.get('fecha')
        manto = Mantenimiento.objects.filter(fecha=fecha)
        data = serializers.serialize('json', manto, fields={'fecha','aplicado', 'descripcion'})
    else:
        data='fail'
    return HttpResponse(data, content_type='application/json')
    