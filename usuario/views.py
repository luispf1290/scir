# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

## libresrias para el sign up
from django.contrib.auth import login, authenticate

### importacion de los formularios
from usuario.forms import UserForm 

from usuario.models import User

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