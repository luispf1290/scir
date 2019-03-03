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
from area import views
from area.views import (AreaCreateView,
						 AreaDeleteView,
						 AreaListView,
						 AreaUpdateView)

urlpatterns = [
	url(r'^nueva/', login_required(AreaCreateView.as_view()), name='newArea'),
	url(r'^lista/areas', login_required(AreaListView.as_view()), name='listAreas'),
	url(r'^modificar/area/(?P<pk>\d+)', login_required(AreaUpdateView.as_view()), name='updateArea'),
	url(r'^eliminar/area/(?P<pk>\d+)', login_required(AreaDeleteView.as_view()), name='deleteArea'),
	url(r'^menu-areas/', login_required(views.menuAreas), name='menu_areas')
]


