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
from solicitud import views
from solicitud.views import RegistroCreateView, ReporteSolicitud
from django.contrib.auth.decorators import login_required

urlpatterns =[
	
    url(r"^servicio/", login_required(RegistroCreateView.as_view()), name="newSolicitud"),
	# url(r'^excelfile/', login_required(ExcelExport.as_view()), name='excelfile'),
	# url(r'^reporte/',login_required(Reporte.as_view()) , name='reporte'),
	url(r'^menu-report/', login_required(views.menu_report), name='menu_report'),
    # url(r'^ajax/solicitud/', login_required(views.SolAjax), name='solajax'),
	url(r'^solicitud-pdf/$', ReporteSolicitud.as_view(), name='solicitud_pdf')
	
]