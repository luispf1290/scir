"""lavanderia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from insumos import views

from insumos.views import InsumosCreateView, InsumosDeleteView, InsumosListView, InsumosUpdateView

urlpatterns = [
	url(r'^nuevo/insumos/', login_required(InsumosCreateView.as_view()), name='newInsumo'),
	url(r'^lista/insumos/$', login_required(InsumosListView.as_view()), name='listInsumo'),
	url(r'^editar/insumos/(?P<pk>\d+)', login_required(InsumosUpdateView.as_view()), name='updateInsumo'),
	url(r'^eliminar/insumos/(?P<pk>\d+)', login_required(InsumosDeleteView.as_view()), name='deleteInsumo'),

    ##### url del ajax ####
    url(r'^insumo/detalle/$', views.DetailAjax, name='home')    

]