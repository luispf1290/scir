# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect


from django.views.generic.edit import (
		CreateView,
		UpdateView,
		DeleteView
	)

from django.views.generic import ListView

##importar modelos
from solicitud.models import Solicitud, Turno, Integral 
from prendas.models import Prendas
from area.models import Area

## importar formularios
from solicitud.forms import SolicitudForm, IntegralForm, Integral_Solicitud_Formset 

# Create your views here.
import time
from datetime import datetime
from django.db.models import Sum
from django.db.models.expressions import RawSQL
from django.db.models.functions import Lower

def menu_report(request):
    return render(request, 'menus/menuReporte.html')

class RegistroCreateView(CreateView):
    model = Integral
    template_name = "solicitud/servicio.html"
    form_class = IntegralForm
    succes_url = reverse_lazy('solicitud:newSolicitud')
    query_prenda = Prendas.objects.all().order_by('id')
    

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        integral_solicitud_form = Integral_Solicitud_Formset()

        return self.render_to_response(self.get_context_data(form=form, integral_solicitud_form=integral_solicitud_form, prenda = self.query_prenda))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        integral_solicitud_form_set = Integral_Solicitud_Formset(request.POST)

        if form.is_valid() and integral_solicitud_form_set.is_valid():
            return self.form_valid(form, integral_solicitud_form_set)
        else:
            return self.form_invalid(form, integral_solicitud_form_set)
    
    def form_valid(self, form, integral_solicitud_form_set):
        self.object = form.save()
        integral_solicitud_form_set.instance = self.object
        integral_solicitud_form_set.save()
        return HttpResponseRedirect(self.succes_url)
    
    def form_invalid(self, form, integral_solicitud_form_set):
        return self.render_to_response(self.get_context_data(form=form, integral_solicitud_form_set=integral_solicitud_form_set))


from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib import colors, styles 
from reportlab.lib.colors import white, black
from reportlab.lib.styles import getSampleStyleSheet
from django.views.generic import View

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

###### reporte de solicitud PDF
class ReporteSolicitud(View):
    """docstring for ReporteSolicitud"""
    x = datetime.now()
    fecha_actual = ("%s-%s-%s"%(x.year,x.month,x.day))
    fecha_actual = str(fecha_actual)
    

    def cabecera(self, c):
        #dibujando la cabecera del PDF
        c.setLineWidth(.3)

        imagen = settings.MEDIA_ROOT+'/imagenes/logo-secretaria-salud.png'
        iner_img = settings.MEDIA_ROOT+'/imagenes/INER.jpg'
        c.drawImage(imagen, 20, 710, 130, 140, preserveAspectRatio=True)
        c.drawImage(iner_img, 450, 740, 120, 90, preserveAspectRatio=True)

        c.setFont('Helvetica', 8)
        c.drawString(187, 800, 'INSTITUTO NACIONAL DE ENFERMEDADES RESPIRATORIAS')
        c.drawString(247,790, 'ISMAEL COLOSIO VILLEGAS')
        c.drawString(237,780, 'DIRECCION DE ADMINISTRACION')
        c.drawString(167,770, 'SUBDIRECCION DE RECURSOS MATERIALES Y SERVICIOS GENERALES')
        c.drawString(157,760, 'DEPARTAMENTO DE MANTENIMIENTO, CONSERVACION Y CONSTRUCCION')
        c.drawString(212,750, 'COORDINACION DE SERVICIOS DE LAVANDERIA')
        c.setFont('Helvetica', 12)
        c.drawString(181, 730, 'SOLICITUD DE SERVICIO A LAVANDERIA')

    def fechayServ(self, c):
        # encabezado = Integral.objects.filter(folio='34089').values('folio').first().get()
        nom_area  = Area.objects.filter(id='1').values('nombre_area').get()
        ## fecha
        cx = 36
        cy = 680
        ancho = 30
        alto = 20

        c.setFillColor(white)
        c.rect(cx, cy, ancho , alto, fill=1)
        c.rect(cx+ancho, cy, ancho, alto, fill=1)
        c.rect(cx+(ancho*2), cy, ancho, alto, fill=1)

        ### Servicio
        c.rect(cx+200, cy, ancho+100, alto, fill=1)
        c.setFillColor(black)
        c.setFont('Helvetica', 10)
        c.drawString(cx+210, cy+6.5,"SERVICIO: "+nom_area['nombre_area'])

        #### Folio
        c.setFillColor(white)
        c.rect(cx+380, cy, ancho+100, alto, fill=1)
        c.setFillColor(black)
        c.setFont('Helvetica', 10)
        c.drawString(cx+390, cy+6.5,"FOLIO: ")

    def recTurnos(self, c):
        cx = 36
        cy = 638
        ancho = 176
        alto = 20

        c.setFillColor(white)
        c.rect(cx, cy, ancho, alto, fill=1)
        c.setFillColor(black)
        c.setFont('Helvetica', 12)
        c.drawString(cx+60, cy+5.5, "MATUTINO")

        c.setFillColor(white)
        c.rect(cx+ancho, cy, ancho, alto, fill=1)
        c.setFillColor(black)
        c.setFont('Helvetica', 12)
        c.drawString(cx+(ancho+55), cy+5.5, "VESPERTINO")

        c.setFillColor(white)
        c.rect(cx+(ancho*2), cy, ancho, alto, fill=1)
        c.setFillColor(black)
        c.setFont('Helvetica', 12)
        c.drawString(cx+((ancho*2)+65), cy+5.5, "VELADA")
    

    def recoleccion(self, c):
         
         cx = 98
         cy =618
         ancho = 57
         alto = 20

         #### linea 

         c.line(cx-62, cy, cx-62, cy+20)

         ### Turno Matutino Primera recoleccion
         c.setFillColor(white)
         c.rect(cx, cy, ancho, alto, fill=1)

         c.setFillColor(black)
         c.setFont('Helvetica', 6.5)
         c.drawString(cx+17, 630, "Primera")
         c.drawString(cx+13, 623, "recoleccion")

         ## Turno matutino segunda recollecion
         c.setFillColor(white)
         c.rect(cx+57, cy, ancho, alto, fill=1)

         c.setFillColor(black)
         c.setFont('Helvetica', 6.5)
         c.drawString(cx+73, 630, "Segunda")
         c.drawString(cx+69.5, 623, "recoleccion")

         ## Turno Vespertino Primera recoleccion
         c.setFillColor(white)
         c.rect(cx+176, cy, ancho, alto, fill=1)

         c.setFillColor(black)
         c.setFont('Helvetica', 6.5)
         c.drawString(cx+194, 630, "Primera")
         c.drawString(cx+189, 623, "recoleccion")

         ## Turno Vespertino segunda recoleccion
         c.setFillColor(white)
         c.rect(cx+232.5, cy, ancho, alto, fill=1)

         c.setFillColor(black)
         c.setFont('Helvetica', 6.5)
         c.drawString(cx+248, 630, "Segunda")
         c.drawString(cx+245.5, 623, "recoleccion")


         ## Turno velada Primera Recoleccion
         c.setFillColor(white)
         c.rect(cx+351.6, cy, ancho, alto, fill=1)

         c.setFillColor(black)
         c.setFont('Helvetica', 6.5)
         c.drawString(cx+368, 630, "Primera")
         c.drawString(cx+363, 623, "recoleccion")

         #Turno velada segunda recoleccion
         c.setFillColor(white)
         c.rect(cx+408.1, cy, ancho, alto, fill=1)

         c.setFillColor(black)
         c.setFont('Helvetica', 6.5)
         c.drawString(cx+422, 630, "Segunda")
         c.drawString(cx+419, 623, "recoleccion")


    def tablalav(self, c, y):
        solicitud_1 = Solicitud.objects.filter(fk_integral__folio='34089',fk_integral__fk_turno='2', fk_integral__fk_recol='1').values('fk_prenda__nombre_prenda','recibe_serv','recibe_lav')
        
        #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 3

        lav_ropa = Paragraph('', styleBH)
        recibe_lav_recol = Paragraph('recibe lav', styleBH)
        recibe_serv_recol = Paragraph('recibe serv' , styleBH)

        data = []
        data.append([lav_ropa, recibe_lav_recol, recibe_serv_recol])
        
         #Table
        width, heigth = A4
        high = 600

        for sol in solicitud_1:
            this_sol = [sol['fk_prenda__nombre_prenda'], 
                        sol['recibe_lav'], 
                        sol['recibe_serv']]
            data.append(this_sol)
            high = high - 18

         #Table size
        width, heigth = A4
        table = Table(data, colWidths=[2.2 * cm, 1 * cm, 1* cm])
        table.setStyle(TableStyle([
             ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
             ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
             ('FONTSIZE', (0, 0), (-1, -1), 8)]))

         #pdf size
        table.wrapOn(c, width, heigth)
        table.drawOn(c, 36, high)
    
    def tabla2(self, c, y):
        solicitud_2 = Solicitud.objects.filter(fk_integral__folio='34089',fk_integral__fk_turno='2', fk_integral__fk_recol='2').values('recibe_serv','recibe_lav')
        #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 3
        recibe_lav_recol = Paragraph('recibe lav', styleBH)
        recibe_serv_recol = Paragraph('recibe serv' , styleBH)

        data = []
        data.append([recibe_lav_recol, recibe_serv_recol])

        width, heigth = A4
        high = 600

        for sol in solicitud_2:
            this_sol = [sol['recibe_lav'], 
                        sol['recibe_serv']]
            data.append(this_sol)
            high = high - 18
        

         #Table size
        width, heigth = A4
        table = Table(data, colWidths=[1 * cm, 1* cm])
        table.setStyle(TableStyle([
             ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
             ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
             ('FONTSIZE', (0, 0), (-1, -1), 8)]))

         #pdf size
        table.wrapOn(c, width, heigth)
        table.drawOn(c, 155, high)

    def tabla3(self, c, y):
        solicitud_1 = Solicitud.objects.filter(fk_integral__folio='34089',fk_integral__fk_turno='2', fk_integral__fk_recol='1').values('fk_prenda__nombre_prenda','recibe_serv','recibe_lav')
        
        #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 3

        lav_ropa = Paragraph('', styleBH)
        recibe_lav_recol = Paragraph('recibe lav', styleBH)
        recibe_serv_recol = Paragraph('recibe serv' , styleBH)

        data = []
        data.append([lav_ropa, recibe_lav_recol, recibe_serv_recol])
        
         #Table
        width, heigth = A4
        high = 600

        for sol in solicitud_1:
            this_sol = [sol['fk_prenda__nombre_prenda'], 
                        sol['recibe_lav'], 
                        sol['recibe_serv']]
            data.append(this_sol)
            high = high - 18

         #Table size
        width, heigth = A4
        table = Table(data, colWidths=[2.2 * cm, 1 * cm, 1* cm])
        table.setStyle(TableStyle([
             ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
             ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
             ('FONTSIZE', (0, 0), (-1, -1), 8)]))

         #pdf size
        table.wrapOn(c, width, heigth)
        table.drawOn(c, 212, high)
    
    def tabla4(self, c, y):
        solicitud_2 = Solicitud.objects.filter(fk_integral__folio='34089',fk_integral__fk_turno='2', fk_integral__fk_recol='2').values('recibe_serv','recibe_lav')
        #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 3
        recibe_lav_recol = Paragraph('recibe lav', styleBH)
        recibe_serv_recol = Paragraph('recibe serv' , styleBH)

        data = []
        data.append([recibe_lav_recol, recibe_serv_recol])

        width, heigth = A4
        high = 600

        for sol in solicitud_2:
            this_sol = [sol['recibe_lav'], 
                        sol['recibe_serv']]
            data.append(this_sol)
            high = high - 18
        

         #Table size
        width, heigth = A4
        table = Table(data, colWidths=[1 * cm, 1* cm])
        table.setStyle(TableStyle([
             ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
             ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
             ('FONTSIZE', (0, 0), (-1, -1), 8)]))

         #pdf size
        table.wrapOn(c, width, heigth)
        table.drawOn(c, 331, high)
    
    
    def tabla5(self, c, y):
        solicitud_1 = Solicitud.objects.filter(fk_integral__folio='34089',fk_integral__fk_turno='2', fk_integral__fk_recol='1').values('fk_prenda__nombre_prenda','recibe_serv','recibe_lav')
        
        #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 3

        lav_ropa = Paragraph('', styleBH)
        recibe_lav_recol = Paragraph('recibe lav', styleBH)
        recibe_serv_recol = Paragraph('recibe serv' , styleBH)

        data = []
        data.append([lav_ropa, recibe_lav_recol, recibe_serv_recol])
        
         #Table
        width, heigth = A4
        high = 600

        for sol in solicitud_1:
            this_sol = [sol['fk_prenda__nombre_prenda'], 
                        sol['recibe_lav'], 
                        sol['recibe_serv']]
            data.append(this_sol)
            high = high - 18

         #Table size
        width, heigth = A4
        table = Table(data, colWidths=[2.2 * cm, 1 * cm, 1* cm])
        table.setStyle(TableStyle([
             ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
             ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
             ('FONTSIZE', (0, 0), (-1, -1), 8)]))

         #pdf size
        table.wrapOn(c, width, heigth)
        table.drawOn(c, 388, high)
    
    def tabla6(self, c, y):
        solicitud_2 = Solicitud.objects.filter(fk_integral__folio='34089',fk_integral__fk_turno='2', fk_integral__fk_recol='2').values('recibe_serv','recibe_lav')
        #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 3
        recibe_lav_recol = Paragraph('recibe lav', styleBH)
        recibe_serv_recol = Paragraph('recibe serv' , styleBH)

        data = []
        data.append([recibe_lav_recol, recibe_serv_recol])

        width, heigth = A4
        high = 600

        for sol in solicitud_2:
            this_sol = [sol['recibe_lav'], 
                        sol['recibe_serv']]
            data.append(this_sol)
            high = high - 18
        

         #Table size
        width, heigth = A4
        table = Table(data, colWidths=[1 * cm, 1* cm])
        table.setStyle(TableStyle([
             ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
             ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
             ('FONTSIZE', (0, 0), (-1, -1), 8)]))

         #pdf size
        table.wrapOn(c, width, heigth)
        table.drawOn(c, 507, high)
    

    def get(self, request, *args, **kwargs):

        date = request.GET.get('fecha')
        area = request.GET.get('area')
        #Indicamos el tipo  de contenido  a devolver en este caso un archivo PDF
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachtment; file_name=prueba_solicitud.pdf'
        #Creando  el objeto PDF utilizando el objeto BytesIO como su archivo
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()

        c = canvas.Canvas(buffer, pagesize=A4)
        self.cabecera(c)
        self.fechayServ(c)
        self.recTurnos(c)
        self.recoleccion(c)
        y=600
        self.tablalav(c, y)
        self.tabla2(c, y)
        self.tabla3(c, y)
        self.tabla4(c,y)
        self.tabla5(c, y)
        self.tabla6(c, y)
        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response



#### reporte total PDF

class Reporte(View):

    succes_url = reverse_lazy('solicitud:menu_report')

    def headerPdf(self, canvas):
        canvas.setLineWidth(.3)

        imagen = settings.MEDIA_ROOT+'/imagenes/logo-secretaria-salud.png'
        iner_img = settings.MEDIA_ROOT+'/imagenes/INER.jpg'
        canvas.drawImage(imagen, 20, 710, 130, 140, preserveAspectRatio=True)
        canvas.drawImage(iner_img, 450, 740, 120, 90, preserveAspectRatio=True)

        canvas.setFont('Helvetica', 8)
        canvas.drawString(187, 800, 'INSTITUTO NACIONAL DE ENFERMEDADES RESPIRATORIAS')
        canvas.drawString(247,790, 'ISMAEL COLOSIO VILLEGAS')
        canvas.drawString(237,780, 'DIRECCION DE ADMINISTRACION')
        canvas.drawString(167,770, 'SUBDIRECCION DE RECURSOS MATERIALES Y SERVICIOS GENERALES')
        canvas.drawString(157,760, 'DEPARTAMENTO DE MANTENIMIENTO, CONSERVACION Y CONSTRUCCION')
        canvas.drawString(212,750, 'COORDINACION DE SERVICIOS DE LAVANDERIA')
        canvas.setFont('Helvetica', 12)
        canvas.drawString(230, 730, 'INFORME DE ACTIVIDADES')
        canvas.setFont('Helvetica', 12)
        canvas.drawString(180, 710, 'Periodo que reporta')

    def table(self, canvas, y):
        
        reportes = []

        peso = [0.80, 0.70, 0.15, 0.35, 0.35, 0.45, 1.50, 0.65, 0.45, 0.25,
                0.10, 0.25, 0.15, 0.05, 0.30, 0.15, 0.35, 0.35, 1.10, 0.75,
                0.75, 0.20, 0.10, 0.40, 1.00]
        
        resultado = []

        prendas = Prendas.objects.values('nombre_prenda')

        

        for prenda in prendas:
            report = Solicitud.objects.filter(fk_integral__fecha__year=2019, fk_prenda__nombre_prenda=prenda['nombre_prenda']).values('fk_prenda__nombre_prenda').annotate(total_ropa=Sum('total_lav')).get()
            
            reportes.append(report)

        j = 0
        while(j < 25):
            resultado.append(reportes[j]['total_ropa'] * peso[j])
            j+=1

         #table header
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 11
        articulo = Paragraph('ARTICULO', styleBH)
        piezas = Paragraph('PIEZAS', styleBH)
        kilos = Paragraph('KILOS' , styleBH)
        data = []
        data.append([articulo, piezas, kilos])
            
         #Table
        width, heigth = A4
        high = 680

        i=0
        while (i < 25):
            data.append([reportes[i]['fk_prenda__nombre_prenda'], reportes[i]['total_ropa'], resultado[i]])
            high = high - 18
            i+=1

        width, heigth = A4
        table = Table(data, colWidths=[10*cm, 4*cm, 4*cm])

        table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
            ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
            ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        
        #pdf size
        table.wrapOn(canvas, width, heigth)
        table.drawOn(canvas, 36, high)

    def totales(self, canvas):
        cx = 320
        cy = 190
        ancho = 113
        alto = 20

        canvas.setFillColor(white)
        canvas.rect(cx, cy, ancho, alto, fill=1)
        canvas.setFillColor(black)
        canvas.setFont('Helvetica', 12)
        canvas.drawString(cx+60, cy+5, "0")

        canvas.setFillColor(white)
        canvas.rect(cx+113, cy, ancho, alto, fill=1)
        canvas.setFillColor(black)
        canvas.setFont('Helvetica', 12)
        canvas.drawString(cx+(ancho+55), cy+5.5, "0")

        ## Pie de pagina
        canvas.setFont('Helvetica', 11)
        canvas.drawString(36, 175,'OBSERVASIONES:')
        canvas.setFont('Helvetica', 10)
        canvas.drawString(36, 155,'En el periodo de ')
        canvas.drawString(125, 155, 'MARZO')
        canvas.drawString(180,155, 'se procesaron')
        canvas.drawString(255, 155,'0')
        canvas.drawString(280,155,'pezas de ropa que hace')
        canvas.drawString(389, 155, 'un total de:')
        canvas.drawString(450, 155, '0')
        canvas.drawString(470, 155, 'kilos;')
        canvas.drawString(36,145, 'para que fuera posible el lavado de ropa, fue necesario el consumo'+ 
            ' de los siguientes productos especiales de limpieza:')
        
        ### Tabla de productos

        articulos= ('REMOVEDOR DE SANGRE', 'AFLOJADOR', 'JABON', 'BLANQUEADOR', 'NEUTRALIZANTE-SUAVIZANTE')
        list_art = []

        for x in range(len(articulos)):
            dic_art = {'articulo' : articulos[x]}

            list_art.append(dic_art)

        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 11
        articulo = Paragraph('DESCRIPCION DEL ARTICULO', styleBH)
        total = Paragraph('TOTAL (Lt, Kg)', styleBH)

        data = [[articulo, total]]
        width, heigth = A4
        high = 100

        for content in list_art:
            this_content = [content['articulo'],]
            data.append(this_content)
            high = high - 18


        table = Table(data, colWidths=[6.5*cm, 3.5*cm])
        table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
            ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
            ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        
        #pdf size
        table.wrapOn(canvas, width, heigth)
        table.drawOn(canvas, 170, high+17)

    def get(self, request, *args, **kwargs):
        
        a = request.GET['anual']
        # b = request.GET['options']
        # c = request.GET['option'] 

        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        y=600
        if(len(a) !=0 ):
            self.headerPdf(c)
            self.table(c,y)
            self.totales(c)
            
        
        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response

    
    



    
