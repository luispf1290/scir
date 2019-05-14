"""manto URL Configuration

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

from manto.views import MantenimientoCreateView, MantenimientoListView
from manto import views

urlpatterns = [
    url(r'^nuevo/', login_required(MantenimientoCreateView.as_view()), name='newManto'),
    url(r'^lista/$', login_required(MantenimientoListView.as_view()), name='listManto'),
    url(r"^lista/(?P<pk>\d+)", login_required(views.MantenimientoRealizadoUpdate), name="checkList"),
    url(r'^fecha_manto/$', login_required(views.fechaManto), name="fechaManto"),
    
]
