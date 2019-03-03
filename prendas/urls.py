"""scir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from prendas.views import (PrendasCreateView, 
							PrendasDeleteView, 
							PrendasListView, 
							PrendasUpdateView)

urlpatterns = [
	url(r'^nueva/', login_required(PrendasCreateView.as_view()), name='newPrenda'),
	url(r'^lista/', login_required(PrendasListView.as_view()), name='listPrenda'),
	url(r'^modificar/(?P<pk>\d+)', login_required(PrendasUpdateView.as_view()), name='updatePrenda'),
	url(r'^eliminar/(?P<pk>\d+)', login_required(PrendasDeleteView.as_view()), name='deletePrenda'),
]