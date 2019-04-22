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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from usuario import views

urlpatterns = [
	url(r'^$', views.index, name='first'),
	url(r'^menu/$', login_required(views.menuPrincipal), name='menuPrincipal'),
    url(r'^admin/', admin.site.urls),
    url(r'^usuario/', include('usuario.urls', namespace='usuario')),
    url(r'^area/', include('area.urls', namespace='area')),
    url(r'^prendas/', include('prendas.urls', namespace = 'prendas')),
    url(r'^insumos/', include('insumos.urls', namespace = 'insumos')),
    url(r'^solicitud/', include('solicitud.urls', namespace='solicitud')),
    url(r'^mantenimiento', include('manto.urls', namespace='manto')),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
