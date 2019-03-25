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


#### crear archivo xls(excel)
#### reporte total PDF

class Reporte(View):
    
    """docstring for Reporte"""
    def encabezado(self, pdf):
        pdf.setLineWidth(.3)
        iner_logo = settings.MEDIA_ROOT+'/imagenes/INER.jpg'
        pdf.drawImage(iner_logo, 500, 750, 60, 60, preserveAspectRatio=True)

        pdf.setFont('Helvetica', 12)
        pdf.drawString(107, 795, 'INSTITUTO NACIONAL DE ENFERMEDADES RESPIRATORIAS')
        pdf.drawString(200,780, 'DIRECCION DE ADMINISTRACION')
        pdf.drawString(60,765, 'SUBDIRECCION DE RECURSOS MATERIALES Y SERVICIOS GENERALES')
        pdf.drawString(50,750, 'DEPARTAMENTO DE MANTENIMIENTO, CONSERVACION Y CONSTRUCCION')
        pdf.drawString(202,735, 'OFICINA DE LAVANDERIA')
        pdf.drawString(181, 715, 'INFORME MENSUAL DE ACTIVIDADES')
        pdf.drawString(50, 690, 'PERIODO QUE REPORTA: ')
        pdf.drawString(230, 690, 'JUNIO')
        pdf.line(220, 685, 280, 685)
        pdf.drawString(300, 690,'DEL: ')
        pdf.drawString(360, 690, '2018')
        pdf.line(355, 685, 395, 685)

    def table(self, pdf, y):
        prendas =('SABANA','COLCHA', 'FUNDA P/ ALMOHADA ', 'PANTALON PIJAMA ADULTO','CAMISA PIJAMA ADULTO',
                    'CAMISON', 'COBERTOR', 'BATA DE MANGA LARGA', 'COMPRESA DOBLE DE 120x120 CMS.', 'COMPRESA DOBLE DE 80X80 CMS.', 'COMPRESA DOBLE DE 40X40 CMS.',
                    'COMPRESA SENCILLA DE 120X120 CMS.', 'COMPRESA SENCILLA DE 80X80 CMS.', 'COMPRESA SENCILLA DE 40X40 CMS.', 'FUNDA P/ MESA DE MAYO', 'COMPRESA PARA RAQUEA', 'SACO PARA CIRUJANO', 'PANTALON PARA CIRUJANO',
                    'SABANA HENDIDA', 'SABAN DE RIÑON', 'SABANA DE PIE', 'BOTA DE LONA', 'TOALLA PARA MANOS', 'PIJAMA INFANTIL', 'MANTEL')
        
        list_cont =[]
        for x in range(len(prendas)):
            dic_cont = {'prenda' : prendas[x]}

            list_cont.append(dic_cont)


        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.fontSize = 11
        articulo = Paragraph('ARTICULO', styleBH)
        piezas = Paragraph('PIEZAS', styleBH)
        kilos = Paragraph('KILOS' , styleBH)

        data = [[articulo, piezas, kilos]]
        width, heigth = A4
        high = 650

        for content in list_cont:
            this_content = [content['prenda'],]
            data.append(this_content)
            high = high - 18


        table = Table(data, colWidths=[10*cm, 4*cm, 4*cm])

        table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
            ('BOX', (0,0), (-1, -1), 0.25, colors.black ),
            ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        
        #pdf size
        table.wrapOn(pdf, width, heigth)
        table.drawOn(pdf, 36, high)

    def pie(self, pdf):
        cx = 320
        cy = 170
        ancho = 113
        alto = 20

        pdf.setFillColor(white)
        pdf.rect(cx, cy, ancho, alto, fill=1)
        pdf.setFillColor(black)
        pdf.setFont('Helvetica', 12)
        pdf.drawString(cx+60, cy+5.5, "0")

        pdf.setFillColor(white)
        pdf.rect(cx+ancho, cy, ancho, alto, fill=1)
        pdf.setFillColor(black)
        pdf.setFont('Helvetica', 12)
        pdf.drawString(cx+(ancho+55), cy+5.5, "0")

        pdf.setFont('Helvetica', 11)
        pdf.drawString(36, 150, 'OBSERVACIONES:')
        pdf.setFont('Helvetica', 10)
        pdf.drawString(36, 135,'En el periodo de ')
        pdf.drawString(125, 135, 'MARZO')
        pdf.drawString(180,135, 'se procesaron')
        pdf.drawString(255, 135,'0')
        pdf.drawString(280,135,'pezas de ropa que hace')
        pdf.drawString(389, 135, 'un total de:')
        pdf.drawString(450, 135, '0')
        pdf.drawString(470, 135, 'kilos;')
        pdf.drawString(36,125, 'para que fuera posible el lavado de ropa, fue necesario el consumo'+ 
            'de los siguientes productos especiales de limpieza:')

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
        table.wrapOn(pdf, width, heigth)
        table.drawOn(pdf, 170, high)


    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize = A4)
        self.encabezado(pdf)
        y = 600
        self.table(pdf, y)
        self.pie(pdf)
        pdf.showPage()
        pdf.save()
        buf = buffer.getvalue()
        buffer.close()
        response.write(buf)
        return response

# import xlsxwriter
# from xlsxwriter.utility import xl_range_abs

# from openpyxl import Workbook
# from openpyxl.drawing.image import Image
# from openpyxl.styles import Font, Alignment

# #### Reporte de solicitud xls(Excel)

# class ExcelExport(View):
#     """docstring for ExcelExport"""

#     def cabecera(self, ws):
#         ft = Font(name='Arial', size=6)
#         ws.column_dimensions['A'].width = 4.87
#         ws.column_dimensions['B'].width = 2.91
#         ws.column_dimensions['C'].width = 8.87
#         ws.column_dimensions['D'].width = 3.95
#         ws.column_dimensions['E'].width = 4.87
#         ws.column_dimensions['F'].width = 4.87
#         ws.column_dimensions['G'].width = 4.87
#         ws.column_dimensions['H'].width = 0.62
#         ws.column_dimensions['I'].width = 5.70
#         ws.column_dimensions['J'].width = 3.62
#         ws.column_dimensions['K'].width = 4.87
#         ws.column_dimensions['L'].width = 4.87
#         ws.column_dimensions['M'].width = 4.87
#         ws.column_dimensions['N'].width = 0.70
#         ws.column_dimensions['O'].width = 5.95
#         ws.column_dimensions['P'].width = 3.62
#         ws.column_dimensions['Q'].width = 4.87
#         ws.column_dimensions['R'].width = 4.87
#         ws.column_dimensions['S'].width = 4.87
#         ws.column_dimensions['T'].width = 0.45
#         ws.column_dimensions['U'].width = 2.66
#         ws.column_dimensions['V'].width = 2.66


#         ws['C2'] = "INSTITUTO NACIONAL DE ENFERMEDADES RESPIRATORIAS"
#         ws.merge_cells('C2:Q2')
#         c2 = ws['C2']
#         c2.font = ft

#         ws['C3'] = 'ISMAEL COLOSIO VILLEGAS'
#         ws.merge_cells('C3:Q3')
#         ws['C3'].font = ft
        
#         ws['C4'] = 'DIRECCIÓN DE ADMINISTRACIÓN'
#         ws.merge_cells('C4:Q4')
#         ws['C4'].font = ft

#         ws['C5'] = 'SUBDIRECCIÓE RECURSOS MATERIALES Y SERVICIOS GENERALES'
#         ws.merge_cells('C5:Q5')
#         ws['C5'].font = ft
        
#         ws['C6'] = 'DEPARTAMENTO DE MANTENIMIENTO, CONSERVACIÓN Y CONSTRUCCIÓN'
#         ws.merge_cells('C6:Q6')
#         ws['C6'].font = ft
        
#         ws['C7'] = 'COORDINACIÓN DE SERVICIOS DE LAVANDERÍA'
#         ws.merge_cells('C7:Q7')
#         ws['C7'].font = ft

#         ft = Font(name = 'Arial', size = 9)
#         ws['A9'] = 'DIA'
#         ws['A9'].font = ft
#         ws['B9'] = 'MES'
#         ws.merge_cells('B9:C9')
#         ws['B9'].font = ft
#         ws['D9'] = 'AÑO'
#         ws['D9'].font = ft
#         ws['E9'] = 'SOLICITUD DE SERVICIO A LAVANDERÍA'
#         ws['E9'].font = ft
#         ws.merge_cells('E9:Q9')
#         ws['R9'] = 'FOLIO:'
#         ws['R9'].font = ft
    
#     def titulos(self, ws):

#         # Turnos
#         ft = Font(name='Arial', size=12)

#         ws['B16'].font = ft
#         ws.merge_cells('B16:G16')
#         ws['B16'] = 'MATUTINO'
        
#         ws['I16'].font = ft
#         ws.merge_cells('I16:M16')
#         ws['I16'] = 'VESPERTINO'
        
#         ws['O16'].font = ft
#         ws.merge_cells('O16:S16')
#         ws['O16'] = 'VELADA'

#         #Recolecciones
#         ft = Font(name='Arial', size=9)

#         # Matutino
#         ws['C17'].font = ft
#         ws.merge_cells('C17:D17')
#         ws['C17'] = '1° RECOLECCIÓN'

#         ws['E17'].font = ft
#         ws.merge_cells('E17:G17')
#         ws['E17'] = '2° RECOLECCIÓN'

#         #Vespertino
#         ws['I17'].font = ft
#         ws.merge_cells('I17:K17')
#         ws['I17'] = '1° RECOLECCIÓN'

#         ws['L17'].font = ft
#         ws.merge_cells('L17:M17')
#         ws['L17'] = '2° RECOLECCIÓN'

#         # Velada
#         ws['O17'].font = ft
#         ws.merge_cells('O17:Q17')
#         ws['O17'] = '1° RECOLECCIÓN'

#         ws['R17'].font = ft
#         ws.merge_cells('R17:S17')
#         ws['R17'] = '2° RECOLECCIÓN'

#         #recibe 
#         ft = Font(name='Arial', size=6 )

#         ws['C18'].font = ft
#         ws['C18'] = 'RECIBE ROPA EL SERVICIO'
#         ws['D18'].font = ft
#         ws['D18'] = 'RECIBE LAVANDERIA'

#         ws['E18'].font = ft
#         ws.merge_cells('E18:F18')
#         ws['E18'] = 'RECIBE ROPA EL SERVICIO'
#         ws['G18'].font = ft
#         ws['G18'] = 'RECIBE LAVANDERIA'
#         ########################################

#         ws['I18'].font = ft
#         ws.merge_cells('I18:J18')
#         ws['I18'] = 'RECIBE ROPA EL SERVICIO'
#         ws['K18'].font = ft
#         ws['K18'] = 'RECIBE LAVANDERIA'

#         ws['L18'].font = ft
#         ws['L18'] = 'RECIBE ROPA EL SERVICIO'
#         ws['M18'].font = ft
#         ws['M18'] = 'RECIBE LAVANDERIA'
#         ###############################################

#         ws['O18'].font = ft
#         ws.merge_cells('O18:P18')
#         ws['O18'] = 'RECIBE ROPA EL SERVICIO'
#         ws['Q18'].font = ft
#         ws['Q18'] = 'RECIBE LAVANDERIA'

#         ws['R18'].font = ft
#         ws['R18'] = 'RECIBE ROPA EL SERVICIO'
#         ws['S18'].font = ft
#         ws['S18'] = 'RECIBE LAVANDERIA'   

#     def datos(self, ws):
#         cont = 1
#         prendas =('Sabana','Colcha', 'Funda', 'Pant. Pijama','Cam. pijam',
#                     'Camison', 'Cobertor', 'Bata Quirurg.', 'CD-120', 'CD-80', 'CD-40',
#                     'CS-120', 'CS-80', 'CS-40', 'Fun-Mayo', 'Comp-Raq', 'Saco-Cir', 'Pant-Cir',
#                     'Sab. Hendida', 'Sab. Riñon', 'sab. Pie', 'Bota de lona', 'Toalla', 'Pijama Inf.', 'Mantel')

#         query1 = Solicitud.objects.filter(id_serv_turno_id=1, fecha="fecha_actual ", id_serv_recol_id=1, id_serv_area_id=1).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#         query2 = Solicitud.objects.filter(id_serv_turno_id=1, fecha="fecha_actual ", id_serv_recol_id=1, id_serv_area_id=1).values_list('serv_sabana','serv_colcha','serv_funda','serv_pantalon_pij','serv_camisa_pij',
#                                                                                                          'serv_camison','serv_cobertor','serv_bataquir', 'serv_cd_120','serv_cd_80',
#                                                                                                          'serv_cd_40','serv_cs_120','serv_cs_80','serv_cs_40','serv_fun_mayo',
#                                                                                                          'serv_comp_raquia', 'serv_saco_cir','serv_pant_cir','serv_sab_h','serv_sab_r',
#                                                                                                          'serv_sab_pie','serv_bota','serv_toalla','serv_pij_inf','serv_mantel')

#         query3 = Solicitud.objects.filter(id_serv_turno_id=1, fecha="fecha_actual ", id_serv_recol_id=2, id_serv_area_id=1).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#         query4 = Solicitud.objects.filter(id_serv_turno_id=1, fecha="fecha_actual ", id_serv_recol_id=2, id_serv_area_id=1).values_list('serv_sabana','serv_colcha','serv_funda','serv_pantalon_pij','serv_camisa_pij',
#                                                                                                          'serv_camison','serv_cobertor','serv_bataquir', 'serv_cd_120','serv_cd_80',
#                                                                                                          'serv_cd_40','serv_cs_120','serv_cs_80','serv_cs_40','serv_fun_mayo',
#                                                                                                          'serv_comp_raquia', 'serv_saco_cir','serv_pant_cir','serv_sab_h','serv_sab_r',
#                                                                                                          'serv_sab_pie','serv_bota','serv_toalla','serv_pij_inf','serv_mantel')

#         query5 = Solicitud.objects.filter(id_serv_turno_id=2, fecha="fecha_actual ", id_serv_recol_id=1, id_serv_area_id=1).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#         query6 = Solicitud.objects.filter(id_serv_turno_id=2, fecha="fecha_actual ", id_serv_recol_id=1, id_serv_area_id=1).values_list('serv_sabana','serv_colcha','serv_funda','serv_pantalon_pij','serv_camisa_pij',
#                                                                                                          'serv_camison','serv_cobertor','serv_bataquir', 'serv_cd_120','serv_cd_80',
#                                                                                                          'serv_cd_40','serv_cs_120','serv_cs_80','serv_cs_40','serv_fun_mayo',
#                                                                                                          'serv_comp_raquia', 'serv_saco_cir','serv_pant_cir','serv_sab_h','serv_sab_r',
#                                                                                                          'serv_sab_pie','serv_bota','serv_toalla','serv_pij_inf','serv_mantel')

#         query7 = Solicitud.objects.filter(id_serv_turno_id=2, fecha="fecha_actual ", id_serv_recol_id=2, id_serv_area_id=1).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#         query8 = Solicitud.objects.filter(id_serv_turno_id=2, fecha="fecha_actual ", id_serv_recol_id=2, id_serv_area_id=1).values_list('serv_sabana','serv_colcha','serv_funda','serv_pantalon_pij','serv_camisa_pij',
#                                                                                                          'serv_camison','serv_cobertor','serv_bataquir', 'serv_cd_120','serv_cd_80',
#                                                                                                          'serv_cd_40','serv_cs_120','serv_cs_80','serv_cs_40','serv_fun_mayo',
#                                                                                                          'serv_comp_raquia', 'serv_saco_cir','serv_pant_cir','serv_sab_h','serv_sab_r',
#                                                                                                          'serv_sab_pie','serv_bota','serv_toalla','serv_pij_inf','serv_mantel')

#         query9 = Solicitud.objects.filter(id_serv_turno_id=3, fecha="fecha_actual ", id_serv_recol_id=1, id_serv_area_id=1).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#         query10 = Solicitud.objects.filter(id_serv_turno_id=3, fecha="fecha_actual ", id_serv_recol_id=1, id_serv_area_id=1).values_list('serv_sabana','serv_colcha','serv_funda','serv_pantalon_pij','serv_camisa_pij',
#                                                                                                          'serv_camison','serv_cobertor','serv_bataquir', 'serv_cd_120','serv_cd_80',
#                                                                                                          'serv_cd_40','serv_cs_120','serv_cs_80','serv_cs_40','serv_fun_mayo',
#                                                                                                          'serv_comp_raquia', 'serv_saco_cir','serv_pant_cir','serv_sab_h','serv_sab_r',
#                                                                                                          'serv_sab_pie','serv_bota','serv_toalla','serv_pij_inf','serv_mantel')

#         query11 = Solicitud.objects.filter(id_serv_turno_id=3, fecha="fecha_actual ", id_serv_recol_id=2, id_serv_area_id=1).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#         query12 = Solicitud.objects.filter(id_serv_turno_id=3, fecha="fecha_actual ", id_serv_recol_id=2, id_serv_area_id=1).values_list('serv_sabana','serv_colcha','serv_funda','serv_pantalon_pij','serv_camisa_pij',
#                                                                                                          'serv_camison','serv_cobertor','serv_bataquir', 'serv_cd_120','serv_cd_80',
#                                                                                                          'serv_cd_40','serv_cs_120','serv_cs_80','serv_cs_40','serv_fun_mayo',
#                                                                                                          'serv_comp_raquia', 'serv_saco_cir','serv_pant_cir','serv_sab_h','serv_sab_r',
#                                                                                                          'serv_sab_pie','serv_bota','serv_toalla','serv_pij_inf','serv_mantel')

#         tupla_recol1 = query1[0]
#         serv_tupla_recol1 = query2[0]
#         tupla_recol2 = query3[0]
#         serv_tupla_recol2 = query4[0]

#         ves_recol1 = query5[0]
#         serv_ves_recol1 = query6[0]
#         ves_recol2 = query7[0]
#         serv_ves_recol2 = query8[0]

#         vel_recol1 = query9[0]
#         serv_vel_recol1 = query10[0]
#         vel_recol2 = query11[0]
#         serv_vel_recol2 = query12[0]

#         list_mat = []

#         for i in range(len(tupla_recol1)):
#             l = {'lav_recol1': tupla_recol1[i],
#                  'serv_recol1' : serv_tupla_recol1[i],
#                  'lav_recol2' : tupla_recol2[i],
#                  'serv_recol2' : serv_tupla_recol2[i],
#                  'prendas' : prendas[i],
#                  'ves_recol1': ves_recol1[i],
#                  'serv_ves_recol1': serv_ves_recol1[i],
#                  'ves_recol2': ves_recol2[i],
#                  'serv_ves_recol2': serv_ves_recol2[i],
#                  'vel_recol1': vel_recol1[i],
#                  'serv_vel_recol1':serv_vel_recol1[i],
#                  'vel_recol2': vel_recol2[i],
#                  'serv_vel_recol2':serv_vel_recol2[i]}

#             list_mat.append(l)

#         ft = Font(name='Arial', size=6 )

#         for datos in list_mat:
#             ws.cell(row=cont+18, column=1).value = datos['prendas']
#             ws.merge_cells(start_row=cont+18, start_column=1, end_row=cont+18, end_column=2)
#             ws.cell(row=cont+18,column=3).value = datos['serv_recol1']
#             ws.cell(row=cont+18,column=4).value=datos['lav_recol1']
#             ws.cell(row=cont+18,column=5).value=datos['serv_recol2']
#             ws.cell(row=cont+18,column=7).value=datos['lav_recol2']
#             ws.cell(row=cont+18,column=9).value = datos['serv_ves_recol1']
#             ws.cell(row=cont+18,column=11).value=datos['ves_recol1']
#             ws.cell(row=cont+18,column=12).value=datos['serv_ves_recol2']
#             ws.cell(row=cont+18,column=13).value=datos['ves_recol2']
#             ws.cell(row=cont+18,column=15).value = datos['serv_vel_recol1']
#             ws.cell(row=cont+18,column=17).value=datos['vel_recol1']
#             ws.cell(row=cont+18,column=18).value=datos['serv_vel_recol2']
#             ws.cell(row=cont+18,column=19).value=datos['vel_recol2']

#             cont = cont+1 
            
            

#     def get(self, request, *args, **kwargs):
#         wb = Workbook()
#         ws = wb.active
#         self.cabecera(ws)
#         self.titulos(ws)
#         self.datos(ws)
#         nom_archivo = "Prueba.xlsx"
#         response = HttpResponse(content_type='application/ms-excel')
#         content = "attachment; filename = {0}".format(nom_archivo)
#         response['Content-Disposition'] = content
#         wb.save(response)
#         return response
 
#         """#response['Content-Disposition'] = 'attachtment; file_name=reporte.xlsx'
#         filename = 'excelfile.xlsx'
#         data = list()
#         data.append(('Apple', 25))
#         data.append(('Peach', 28))
#         data.append(('Orange', 17))

#         #creando y abriendo el archivo
#         wb = xlsxwriter.Workbook(filename)

#         #agregando el Worksheet

#         sheet = wb.add_worksheet('Hoja1')

#         # enviar los formatos

#         section_header_format = wb.add_format({
#             'bold' : True,
#             'align' : 'left',
#             'font_size' : 16,
#             })

#         # definir el formato numero

#         num_format = wb.add_format({
#             'num_format' : '0',
#             'align' :'rigth',
#             'font_size' : 12,
#             })

#         #definir formato general
#         general_format = wb.add_format({
#             'align' : 'left',
#             'font_size' : 12,
#             })

#         # define el ancho de las columnas

#         sheet.set_column(0, 0, 45, general_format)
#         sheet.set_column(1, 1, 20, num_format)

#         #agregamos un titulo al encabezado
#         # inicia_fila, inicia_col, termina_fila, termina_col, titulo, formato

#         sheet.merge_range(6, 0, 6, 1, "Ejemplo de archivo xls", section_header_format)

#         #ponemos encabezados  en las columnas
#         row = 8
#         sheet.write(row, 0, 'Fruta')
#         sheet.write(row, 1, 'Cantidad')

#         # colocamos  los datos de la lista que creamos al inicio del metodo get
#         # Por medio de un for recorremos y copiamos cada objetos y tuplas

#         for obj in data:
#             row += 1
#             sheet.write_row(row, 0, obj)

#         # cerramos el archivo
#         wb.close()

#         #retornamos el response
        
#         #return HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         return HttpResponse(content_type='application/ms-excel') """

# from django.core import serializers
# import json

# def SolAjax(request):
#     model = Solicitud
#     area = request.GET.get('area')
#     turno = request.GET.get('turno')
#     recol = request.GET.get('recol')
#     print(area)
#     print(turno)
#     print(recol)

#     solicitud = model.objects.filter(id_serv_turno_id=1,
#                                     fecha="2018-05-28",
#                                     id_serv_recol_id=recol,
#                                     id_serv_area_id=area).values_list('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel')

#     datos = serializers.serialize('json', solicitud, fields=('lav_sabana','lav_colcha','lav_funda','lav_pantalon_pij','lav_camisa_pij',
#                                                                                                          'lav_camison','lav_cobertor','lav_bataquir', 'lav_cd_120','lav_cd_80',
#                                                                                                          'lav_cd_40','lav_cs_120','lav_cs_80','lav_cs_40','lav_fun_mayo',
#                                                                                                          'lav_comp_raquia', 'lav_saco_cir','lav_pant_cir','lav_sab_h','lav_sab_r',
#                                                                                                          'lav_sab_pie','lav_bota','lav_toalla','lav_pij_inf','lav_mantel'))
#     return HttpResponse(datos, content_type='application/json')