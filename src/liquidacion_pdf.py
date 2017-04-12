#!/usr/bin/env python
  
############################################################################
#    Copyright (C) 2005 by												   #
#                                                                          #
#        Milton Inostroza Aguilera         						           #
#           minoztro@gmail.com               					           #
#                                                                          #
#    This class is free software; you can redistribute it and#or modify    #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                    #
#                                                                          #
#    This class is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import *
from reportlab.lib.colors import *
from reportlab.lib.units import mm

import sys
import os
import calendar
from numeros_a_letras import *

class Liquidacion_pdf:

	def __init__(self, datos, padre):
		
		self.datos=datos
		self.padre=padre
		c = canvas.Canvas("LIQUIDACION_SUELDO_%s_%s_%s.pdf"%(self.datos["fecha liquidacion"].strftime("%B").upper(),
															 self.datos["fecha liquidacion"].strftime("%Y"),
															 self.datos["nombre trabajador"]),pagesize=letter,pageCompression=1)
		c.translate(mm,mm)
		#marco pagina
		c.line(5*mm,16*mm,205*mm,16*mm)
		c.line(5*mm,16*mm,5*mm,270*mm)
		c.line(5*mm,270*mm,205*mm,270*mm)
		c.line(205*mm,270*mm,205*mm,16*mm)
		
		#c.drawImage('pixmaps/Remunex.jpg',5*mm,272*mm)

		#cuerpo cabecera
		c.setFont('Courier',20)
		c.drawCentredString(102.5*mm,263*mm,"LIQUIDACION DE SUELDO")
		c.line(5*mm,260*mm,205*mm,260*mm)
		c.setFillColor(lightgrey)
		c.rect(5*mm,255*mm,200*mm,5*mm, fill=1)
		
		c.setFillColor(black)
		c.setFont('Courier',12)
		c.drawString(10*mm,250*mm,"Nombre: %s"%(self.datos["nombre trabajador"]))
		c.drawString(153*mm,250*mm,"R.U.T.: %s"%(self.datos["rut trabajador"]))
		c.line(5*mm,247*mm,205*mm,247*mm)
		c.setFillColor(lightgrey)
		c.rect(5*mm,242*mm,200*mm,5*mm, fill=1)
		
		c.setFillColor(black)
		c.setFont('Courier',16)
		c.drawCentredString(102.5*mm,236*mm,"DETALLE DE LA REMUNERACION")
		c.line(5*mm,233*mm,205*mm,233*mm)
		
		#cuerpo detalle remuneracion
		c.setFont('Courier',12)
		c.drawString(15*mm,225*mm,"%s Dias"%(self.datos["dias trabajados"]))
		c.drawString(40*mm,225*mm,"Sueldo Base mes de %s %s"%(self.datos["fecha liquidacion"].strftime("%B"),
															   self.datos["fecha liquidacion"].strftime("%Y")))
		c.drawRightString(203*mm,225*mm,"$%s.-"%(self.formato_numero_miles(self.datos["sueldo base"])))
		
		c.drawString(40*mm,220*mm,"Bono de viajes")
		c.drawRightString(203*mm,220*mm,"$%s.-"%(self.formato_numero_miles(self.datos["bono de viajes"])))

		#c.drawString(15*mm,215*mm,"yy Horas")
		#c.drawString(40*mm,215*mm,"Feriado anual periodo 2004-05 valor dia $5.333.-")
		#c.drawRightString(203*mm,215*mm,"$0.-")
		
				
		c.setFont('Courier',14)
		c.drawString(10*mm,205*mm,"TOTAL IMPONIBLE")
		c.drawRightString(203*mm,205*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total imponible"]))))
		c.rect(5*mm,203*mm,200*mm,7*mm)
		
		c.setFont('Courier',12)
		if not self.datos["numero de cargas"]=='0':
			c.drawString(15*mm,195*mm,"%s %s"%(self.datos["numero de cargas"],numerals(self.datos["numero de cargas"],False)))
			c.drawString(40*mm,195*mm,"Cargas de Asignacion Familiar valor carga $0.-")
			c.drawRightString(203*mm,195*mm,"$%s.-"%(self.formato_numero_miles(self.datos["total cargas"])))
		
		c.drawString(40*mm,190*mm,"Viatico")
		c.drawRightString(203*mm,190*mm,"$%s.-"%(self.formato_numero_miles(self.datos["viatico"])))
		
		c.drawString(40*mm,185*mm,"Movilizacion")
		c.drawRightString(203*mm,185*mm,"$%s.-"%(self.formato_numero_miles(self.datos["movilizacion"])))
		
		c.setFont('Courier',14)
		c.drawString(10*mm,175*mm,"SUB TOTAL")
		c.drawRightString(203*mm,175*mm,"$%s.-"%(self.formato_numero_miles((str(self.datos["sub total"])))))
		c.rect(5*mm,173*mm,200*mm,7*mm)
		
		c.setFont('Courier',14)
		c.drawString(10*mm,168*mm,"TOTAL HABER")
		c.drawRightString(203*mm,168*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total haber"]))))
		c.rect(5*mm,166*mm,200*mm,7*mm)
		
		#descuentos de cargo del trabajador
		c.setFont('Courier',16)
		c.drawCentredString(102.5*mm,160*mm,"DESCUENTOS DE CARGO DEL TRABAJADOR")
		c.line(5*mm,157*mm,205*mm,157*mm)
		
		c.setFont('Courier',12)
		c.drawString(40*mm,150*mm,"A.F.P.")
		c.drawString(95*mm,150*mm,": %s %s%s"%(self.datos["nombre afp"],self.datos["porcentaje afp"],'%'))
		c.drawRightString(203*mm,150*mm,"$%s.-"%(self.formato_numero_miles(self.datos["cotizacion obligatoria"])))
		
		if not self.datos.has_key("adicional pactado"):
			c.drawString(40*mm,145*mm,"Sistema Salud")
			c.drawString(95*mm,145*mm,": %s %s%s"%(self.datos["salud"], self.datos["porcentaje salud"],'%'))
			c.drawRightString(203*mm,145*mm,"$%s.-"%(self.formato_numero_miles((self.datos["descuento salud"]))))
		else:
			c.drawString(40*mm,145*mm,"Sistema Salud")
			c.drawString(95*mm,145*mm,": %s A.P. %s U.F."%(self.datos["salud"], self.datos["cantidad uf"]))
			c.drawString(95*mm,140*mm,"  Valor U.F.: $%s.-"%(self.datos["valor uf"]))
			c.drawRightString(203*mm,145*mm,"$%s.-"%(self.formato_numero_miles(self.datos["adicional pactado"])))

		linea=135
		if self.datos.has_key("porcentaje seguro cesantia"):
			c.drawString(40*mm,linea*mm,"Seguro Cesantia")
			c.drawString(95*mm,linea*mm,"  %s%s"%(self.datos["porcentaje seguro cesantia"],'%'))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["valor seguro cesantia"]))))
			linea=linea-5
		
		if self.datos.has_key("ahorro voluntario"):
			c.drawString(40*mm,linea*mm,"Ahorro Voluntario")
			c.drawString(95*mm,linea*mm,"  A.F.P. %s"%(self.datos["nombre afp"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["ahorro voluntario"]))))
			linea=linea-5
			
		if self.datos.has_key("caja compensacion"):
			c.drawString(40*mm,linea*mm,"Prestamo CC.AA.")
			c.drawString(95*mm,linea*mm,"  %s cuota %s"%(self.datos["caja compensacion"], self.datos["prestamo caja cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["prestamo caja valor cuota"])))
			linea=linea-5
			
		if self.datos.has_key("compania seguro"):
			c.drawString(40*mm,linea*mm,"Seguro de Vida CC.AA.")
			c.drawString(95*mm,linea*mm,"  %s cuota %s"%(self.datos["compania seguro"], self.datos["seguro de vida cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%.-"%(self.formato_numero_miles(self.datos["seguro de vida valor cuota"])))
			linea=linea-5
			
		if self.datos.has_key("leasing cuota"):
			c.drawString(40*mm,linea*mm,"Leasing CC.AA.")
			c.drawString(95*mm,linea*mm,"  LOS ANDES cuota %s"%(self.datos["leasing cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["leasing valor cuota"])))
			linea=linea-5
		
		if self.datos.has_key("prestamo fonasa cuota"):
			c.drawString(40*mm,linea*mm,"Prestamo FONASA")
			c.drawString(95*mm,linea*mm,"  cuota %s"%(self.datos["prestamo fonasa cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["prestamo fonasa valor cuota"])))
			linea=linea-5
		
		if self.datos.has_key("prestamo empresa cuota"):
			c.drawString(40*mm,linea*mm,"Prestamo Empresa")
			c.drawString(95*mm,linea*mm,"  cuota %s"%(self.datos["prestamo empresa cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["prestamo empresa valor cuota"])))
			linea=linea-5
			
		if self.datos.has_key("otros descuentos"):
			c.drawString(40*mm,linea*mm,"%s"%(self.datos["otros descuentos"]))
			c.drawString(95*mm,linea*mm,"  cuota 0")
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["otros descuentos valor cuota"])))

		#resumen de indicadores
		c.setFont('Courier',14)
		c.drawString(10*mm,82*mm,"TOTAL DESCUENTOS")
		c.drawRightString(203*mm,82*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total descuentos"]))))
		c.rect(5*mm,80*mm,200*mm,7*mm)
		
		c.drawString(10*mm,75*mm,"ALCANCE LIQUIDO")
		c.drawRightString(203*mm,75*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total haber"]-self.datos["total descuentos"]))))
		c.rect(5*mm,73*mm,200*mm,7*mm)
		
		c.drawString(10*mm,68*mm,"VALES O ANTICIPOS")
		c.drawRightString(203*mm,68*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["vales o anticipos"]))))
		c.rect(5*mm,66*mm,200*mm,7*mm)
		
		c.drawString(10*mm,61*mm,"SALDO LIQUIDO")
		c.drawRightString(203*mm,61*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total haber"]-self.datos["total descuentos"]-int(self.datos["vales o anticipos"])))))
		c.rect(5*mm,59*mm,200*mm,7*mm)
		
		#despedida del documento
		c.setFont('Courier',10)
		c.drawString(10*mm,53*mm,"Certifico que he recibido de")
		c.setFont('Courier',12)
		sql="""SELECT razon_social_representante
		FROM empleador
		WHERE rut_empresa='%s'
		"""%(self.padre.rut_empresa_actual)
		self.padre.cursor.execute(sql)
		r=self.padre.cursor.fetchall()
		c.drawString(70*mm,53*mm," %s"%(r[0][0]))
		
		c.setFont('Courier',10)
		c.drawString(10*mm,49*mm,"a mi entera satisfaccion el saldo liquido indicado en la presente liquidacion")
		c.drawString(10*mm,45*mm,"y no tengo cargo ninguno de los conceptos comprendidos en ella.")
		
		
		#firma de trabajador
		c.setFont('Courier',12)
		c.drawCentredString(153.75*mm,30*mm,"%s"%(self.datos["nombre trabajador"]))
		c.drawCentredString(153.75*mm,25*mm,"R.U.T.: %s"%(self.datos["rut trabajador"]))
		
		#fecha
		c.setFont('Courier',12)
		c.drawString(10*mm,20*mm,"Iquique, ")
		c.drawString(35*mm,20*mm,"%s de %s de %s"%(calendar.monthrange(int(self.datos["fecha liquidacion"].strftime("%Y")),int(self.datos["fecha liquidacion"].strftime("%m")))[1],
													self.datos["fecha liquidacion"].strftime("%B"),
													self.datos["fecha liquidacion"].strftime("%Y")))
		c.showPage()
		
		#boleta de sueldo
		
		c.translate(mm,mm)
		
		#marco pagina
		c.line(5*mm,16*mm,205*mm,16*mm)
		c.line(5*mm,16*mm,5*mm,270*mm)
		c.line(5*mm,270*mm,205*mm,270*mm)
		c.line(205*mm,270*mm,205*mm,16*mm)

		c.setFont('Courier',20)
		c.drawCentredString(102.5*mm,263*mm,"BOLETA DE SUELDO %s %s"%((self.datos["fecha liquidacion"].strftime("%B")).upper(),
													self.datos["fecha liquidacion"].strftime("%Y")))
		c.line(5*mm,260*mm,205*mm,260*mm)
		c.setFillColor(lightgrey)
		c.rect(5*mm,255*mm,200*mm,5*mm, fill=1)
		
		c.setFillColor(black)
		c.setFont('Courier',12)
		c.drawString(10*mm,250*mm,"Nombre: %s"%(self.datos["nombre trabajador"]))
		c.drawString(153*mm,250*mm,"R.U.T.: %s"%(self.datos["rut trabajador"]))
		c.line(5*mm,247*mm,205*mm,247*mm)
		c.setFillColor(lightgrey)
		c.rect(5*mm,242*mm,200*mm,5*mm, fill=1)
		
		linea_vueltas=235
		c.setFillColor(black)
		c.setFont('Courier',14)
		c.drawCentredString(102.5*mm,237*mm,"DETALLE DE VIAJES")
		c.line(5*mm,linea_vueltas*mm,205*mm,linea_vueltas*mm)
		linea_vueltas=linea_vueltas-5

		c.setFont('Courier',12)
		c.drawCentredString(50*mm,linea_vueltas*mm,"LUGAR")
		c.drawCentredString(117*mm,linea_vueltas*mm,"Nro. VIAJES")
		c.drawCentredString(150.5*mm,linea_vueltas*mm,"VALOR")
		c.drawCentredString(186*mm,linea_vueltas*mm,"TOTAL")
		linea_vueltas=linea_vueltas-2
		c.line(5*mm,228*mm,205*mm,linea_vueltas*mm)
		
		linea_vueltas=linea_vueltas-5
		if len(self.datos["detalle_vueltas"])==0:
			for i in range(2):
				linea_vueltas=linea_vueltas-5
			
		else:
			for vueltas in self.datos["detalle_vueltas"]:
				c.drawString(10*mm,linea_vueltas*mm,"%s"%(vueltas[1]))
				c.drawCentredString(117*mm,linea_vueltas*mm,"%s"%(vueltas[0]))
				c.drawRightString(165*mm,linea_vueltas*mm,"$%s"%(self.formato_numero_miles(vueltas[2])))
				c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(vueltas[3])))
				linea_vueltas=linea_vueltas-5
		#lineas de separacion bloques
		c.line(100*mm,235*mm,100*mm,(linea_vueltas+3)*mm)
		c.line(134*mm,235*mm,134*mm,(linea_vueltas+3)*mm)
		c.line(167*mm,235*mm,167*mm,(linea_vueltas-4)*mm)
		c.line(5*mm,(linea_vueltas+3)*mm,205*mm,(linea_vueltas+3)*mm)
		linea_vueltas=linea_vueltas-2
		c.setFont('Courier',14)
		c.drawString(10*mm,linea_vueltas*mm,"TOTAL DE VIAJES")
		c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["bono de viajes"])))
		c.line(5*mm,(linea_vueltas-2)*mm,205*mm,(linea_vueltas-2)*mm)
		linea_vueltas=linea_vueltas-8
		
		c.setFont('Courier',12)
		c.drawString(40*mm,linea_vueltas*mm,"Sueldo mes de %s %s"%(self.datos["fecha liquidacion"].strftime("%B"),
															   self.datos["fecha liquidacion"].strftime("%Y")))
		
		c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(str(int(self.datos["sueldo base"])+int(self.datos["bono de viajes"])))))
		linea_vueltas=linea_vueltas-5
		
		if not self.datos["numero de cargas"]=='0':
			c.drawString(15*mm,linea_vueltas*mm,"%s %s"%(self.datos["numero de cargas"],numerals(self.datos["numero de cargas"],False)))
			c.drawString(40*mm,linea_vueltas*mm,"Cargas de Asignacion Familiar valor carga $0.-")
			c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["total cargas"])))
			linea_vueltas=linea_vueltas-5
		
		c.drawString(40*mm,linea_vueltas*mm,"Viatico")
		c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["viatico"])))
		
		linea_vueltas=linea_vueltas-5
		
		c.drawString(40*mm,linea_vueltas*mm,"Movilizacion")
		c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["movilizacion"])))
		
		c.line(5*mm,(linea_vueltas-2)*mm,205*mm,(linea_vueltas-2)*mm)
		linea_vueltas=linea_vueltas-7
		c.setFont('Courier',14)
		c.drawString(10*mm,linea_vueltas*mm,"TOTAL LIQUIDO")
		c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total haber"]))))
		
		c.line(5*mm,(linea_vueltas-2)*mm,205*mm,(linea_vueltas-2)*mm)
		
		linea_vueltas=linea_vueltas-7
		
		c.setFont('Courier',16)
		c.drawCentredString(102.5*mm,linea_vueltas*mm,"DESCUENTOS DE CARGO DEL TRABAJADOR")
		c.line(5*mm,(linea_vueltas-2)*mm,205*mm,(linea_vueltas-2)*mm)
		
		linea_vueltas=linea_vueltas-7
		
		c.setFont('Courier',12)
		c.drawString(40*mm,linea_vueltas*mm,"A.F.P.")
		c.drawString(95*mm,linea_vueltas*mm,": %s %s%s"%(self.datos["nombre afp"],self.datos["porcentaje afp"],'%'))
		c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["cotizacion obligatoria"])))
		
		linea_vueltas=linea_vueltas-5
		
		if not self.datos.has_key("adicional pactado"):
			c.drawString(40*mm,linea_vueltas*mm,"Sistema Salud")
			c.drawString(95*mm,linea_vueltas*mm,": %s %s%s"%(self.datos["salud"], self.datos["porcentaje salud"],'%'))
			c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["descuento salud"])))
		else:
			c.drawString(40*mm,linea_vueltas*mm,"Sistema Salud")
			c.drawString(95*mm,linea_vueltas*mm,": %s A.P. %s U.F."%(self.datos["salud"], self.datos["cantidad uf"]))
			c.drawString(95*mm,linea_vueltas-5*mm,"  Valor U.F.: $%s.-"%(self.datos["valor uf"]))
			c.drawRightString(203*mm,linea_vueltas*mm,"$%s.-"%(self.formato_numero_miles(self.datos["adicional pactado"])))

		linea=linea_vueltas-10
		if self.datos.has_key("porcentaje seguro cesantia"):
			c.drawString(40*mm,linea*mm,"Seguro Cesantia")
			c.drawString(95*mm,linea*mm,"  %s%s"%(self.datos["porcentaje seguro cesantia"],'%'))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["valor seguro cesantia"]))))
			linea=linea-5
		
		if self.datos.has_key("ahorro voluntario"):
			c.drawString(40*mm,linea*mm,"Ahorro Voluntario")
			c.drawString(95*mm,linea*mm,"  A.F.P. %s"%(self.datos["nombre afp"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["ahorro voluntario"])))
			linea=linea-5
			
		if self.datos.has_key("caja compensacion"):
			c.drawString(40*mm,linea*mm,"Prestamo CC.AA.")
			c.drawString(95*mm,linea*mm,"  %s cuota %s"%(self.datos["caja compensacion"], self.datos["prestamo caja cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["prestamo caja valor cuota"])))
			linea=linea-5
			
		if self.datos.has_key("compania seguro"):
			c.drawString(40*mm,linea*mm,"Seguro de Vida CC.AA.")
			c.drawString(95*mm,linea*mm,"  %s cuota %s"%(self.datos["compania seguro"], self.datos["seguro de vida cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%.-"%(self.formato_numero_miles(self.datos["seguro de vida valor cuota"])))
			linea=linea-5
			
		if self.datos.has_key("leasing cuota"):
			c.drawString(40*mm,linea*mm,"Leasing CC.AA.")
			c.drawString(95*mm,linea*mm,"  LOS ANDES cuota %s"%(self.datos["leasing cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["leasing valor cuota"])))
			linea=linea-5
		
		if self.datos.has_key("prestamo fonasa cuota"):
			c.drawString(40*mm,linea*mm,"Prestamo FONASA")
			c.drawString(95*mm,linea*mm,"  cuota %s"%(self.datos["prestamo fonasa cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["prestamo fonasa valor cuota"])))
			linea=linea-5
		
		if self.datos.has_key("prestamo empresa cuota"):
			c.drawString(40*mm,linea*mm,"Prestamo Empresa")
			c.drawString(95*mm,linea*mm,"  cuota %s"%(self.datos["prestamo empresa cuota"]))
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["prestamo empresa valor cuota"])))
			linea=linea-5
			
		if self.datos.has_key("otros descuentos"):
			c.drawString(40*mm,linea*mm,"%s"%(self.datos["otros descuentos"]))
			c.drawString(95*mm,linea*mm,"  cuota 0")
			c.drawRightString(203*mm,linea*mm,"$%s.-"%(self.formato_numero_miles(self.datos["otros descuentos valor cuota"])))
		
		c.setFont('Courier',14)
		c.drawString(10*mm,82*mm,"TOTAL DESCUENTOS")
		c.drawRightString(203*mm,82*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total descuentos"]))))
		c.rect(5*mm,80*mm,200*mm,7*mm)
		
		c.drawString(10*mm,75*mm,"ALCANCE LIQUIDO")
		c.drawRightString(203*mm,75*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total haber"]-self.datos["total descuentos"]))))
		c.rect(5*mm,73*mm,200*mm,7*mm)
		
		c.drawString(10*mm,68*mm,"VALES O ANTICIPOS")
		c.drawRightString(203*mm,68*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["vales o anticipos"]))))
		c.rect(5*mm,66*mm,200*mm,7*mm)
		
		c.drawString(10*mm,61*mm,"SALDO LIQUIDO")
		c.drawRightString(203*mm,61*mm,"$%s.-"%(self.formato_numero_miles(str(self.datos["total haber"]-self.datos["total descuentos"]-int(self.datos["vales o anticipos"])))))
		c.rect(5*mm,59*mm,200*mm,7*mm)
		
		c.setFont('Courier',10)
		c.drawString(10*mm,53*mm,"Certifico que he recibido de")
		c.setFont('Courier',12)
		sql="""SELECT razon_social_representante
		FROM empleador
		WHERE rut_empresa='%s'
		"""%(self.padre.rut_empresa_actual)
		self.padre.cursor.execute(sql)
		r=self.padre.cursor.fetchall()
		c.drawString(70*mm,53*mm," %s"%(r[0][0]))
		
		c.setFont('Courier',10)
		c.drawString(10*mm,49*mm,"a mi entera satisfaccion el saldo liquido indicado en la presente liquidacion")
		c.drawString(10*mm,45*mm,"y no tengo cargo ninguno de los conceptos comprendidos en ella.")
		
		
		#firma de trabajador
		c.setFont('Courier',12)
		c.drawCentredString(153.75*mm,30*mm,"%s"%(self.datos["nombre trabajador"]))
		c.drawCentredString(153.75*mm,25*mm,"R.U.T.: %s"%(self.datos["rut trabajador"]))
		
		#fecha
		c.setFont('Courier',12)
		c.drawString(10*mm,20*mm,"Iquique, ")
		c.drawString(35*mm,20*mm,"%s de %s de %s"%(calendar.monthrange(int(self.datos["fecha liquidacion"].strftime("%Y")),int(self.datos["fecha liquidacion"].strftime("%m")))[1],
													self.datos["fecha liquidacion"].strftime("%B"),
													self.datos["fecha liquidacion"].strftime("%Y")))
		c.showPage()
		c.save()
	
	def formato_numero_miles(self, numero):
		pos=len(numero)
		while pos>3:
			pos=pos-3
			numero=numero[:pos]+'.'+numero[pos:]
		return numero
	
	def Abre_pdf(self,arch):
		if sys.platform=="win32":

			acrord = 'c:\\Archivos de programa\\Adobe\\Acrobat 5.0\\Reader\\AcroRd32.exe'
	
			#~ acrord = "explorer.exe"
			#~ acrord = os.getcwd() + "\\pdfreader\\pdfreader.exe"
	
			args = [acrord, "AcroRd32.exe",arch]
	
			try:
				os.spawnv(os.P_NOWAIT, args[0], args[1:])
				print "acro"
			except:
				acrord = os.getcwd() + "\\pdfreader\\pdfreader.exe"
				args = [acrord, "pdfreader.exe",arch]
				try:
					os.spawnv(os.P_NOWAIT, args[0], args[1:])
					print "PDFReader"
				except:
					print "no hay un visor registrado."
	
	
		else:
			if os.spawnv(os.P_NOWAIT, '/usr/bin/xpdf', ['xpdf', arch]) != 0 :
				print "xPdf"
			elif os.spawnv(os.P_NOWAIT, '/usr/bin/acroread', ['acroread', arch]) != 0 :
				print "acroread"
			elif os.spawnv(os.P_NOWAIT, '/usr/bin/gpdf', ['gpdf', arch]) != 0 :
				print "gPdf"
