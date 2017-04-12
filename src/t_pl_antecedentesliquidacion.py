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
#    (at your option) any later version.                                   #
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

from GladeConnect import GladeConnect
from pyPgSQL.PgSQL import connect
from pyPgSQL import PgSQL
import pygtk
pygtk.require('2.0')
import gtk
from calendario import * 
import re
from viajes_realizados import *
from anticipos import *
from liquidacion_pdf import *

class t_pl_AntecedentesLiquidacion(GladeConnect):
	"agregar comentario"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/t_pl_antecedentesliquidacion.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.rut_trabajador=None
		self.inicio_vacaciones_time=None
		self.fin_vacaciones_time=None
		self.inicio_licencia_time=None
		self.fin_licencia_time=None
		self.inicio_permiso_time=None
		self.fin_permiso_time=None
		self.modelo_vueltas=None
		self.tipo_trabajador=None
		self.codigo_proceso=None
		self.diccionario_caja=[]
		self.diccionario_empresa=[]
		self.diccionario_fonasa=[]
		self.diccionario_otros_descuentos=[]
		self.datos_liquidacion_sueldo={}
		self.regexp=re.compile("[0-9]+'")
		#poniendo cajas no editables
		#antecedentes imponibles
		self.entrySueldoBase.set_sensitive(False)
		self.entryFactorHorasExtras.set_sensitive(False)
		self.entryDiasTrabajados.set_sensitive(False)
		self.entryDiasVacaciones.set_sensitive(False)
		self.entryInicioVacaciones.set_sensitive(False)
		self.toolbuttonInicioVacaciones.set_sensitive(False)
		self.entryFinVacaciones.set_sensitive(False)
		self.toolbuttonFinVacaciones.set_sensitive(False)
		self.entryDiasLicencia.set_sensitive(False)
		self.entryInicioLicencia.set_sensitive(False)
		self.toolbuttonInicioLicencia.set_sensitive(False)
		self.entryFinLicencia.set_sensitive(False)
		self.toolbuttonFinLicencia.set_sensitive(False)
		self.entryDiasPermiso.set_sensitive(False)
		self.entryInicioPermiso.set_sensitive(False)
		self.toolbuttonInicioPermiso.set_sensitive(False)
		self.entryFinPermiso.set_sensitive(False)
		self.toolbuttonFinPermiso.set_sensitive(False)
		
		self.entryHorasExtras.set_sensitive(False)
		self.entryBonoViajes.set_sensitive(False)
		self.toolbuttonVueltas.set_sensitive(False)
		
		#antecedentes no imponibles
		self.entryColacion.set_sensitive(False)
		self.entryMovilizacion.set_sensitive(False)
		self.entryNumeroCargas.set_sensitive(False)
		self.entryTramoCarga.set_sensitive(False)
		self.entryCargasRetroactivas.set_sensitive(False)
		self.entryValorTotal.set_sensitive(False)
		self.entryViaticos.set_sensitive(False)
		
		self.entryDiasVacacionesNoImponibles.set_sensitive(False)
		self.entryInicioVacacionesNoImponibles.set_sensitive(False)
		self.entryFinVacacionesNoImponibles.set_sensitive(False)
		self.toolbuttonInicioVacacionesNoImponibles.set_sensitive(False)
		self.toolbuttonFinVacacionesNoImponibles.set_sensitive(False)

		
		#antecedentes descuentos
		self.entryNombreAfp.set_sensitive(False)
		self.entryTipoAfiliado.set_sensitive(False)
		self.entryCotizacionObligatoria.set_sensitive(False)
		self.entryAhorroVoluntario.set_sensitive(False)
		self.entryOptaSeguroCesantia.set_sensitive(False)
		self.entryPorcientroSeguroDesempleo.set_sensitive(False)
		
		self.entrySalud.set_sensitive(False)
		self.entryDescuentoSalud.set_sensitive(False)
		
		self.entryCompaniaSeguroVidaPosee.set_sensitive(False)
		self.entryCompania.set_sensitive(False)
		self.entryNumeroCuotaCompania.set_sensitive(False)
		self.entryValorCompania.set_sensitive(False)
		
		self.entryRutCodigoInterno.set_sensitive(False)
		self.entryNumeroCuenta.set_sensitive(False)
		self.entryNumeroCuota.set_sensitive(False)
		self.entryAporteUFPorcentajeRemuneracion.set_sensitive(False)
		self.entryAporteDinero.set_sensitive(False)
		
		self.entryCajaSeguroVidaPosee.set_sensitive(False)
		self.entryCajaCompensacion.set_sensitive(False)
		self.entryNumeroCuotaCaja.set_sensitive(False)
		self.entryValorCaja.set_sensitive(False)
		
		self.entryAnticipos.set_sensitive(False)
		self.toolbuttonAnticipos.set_sensitive(False)

		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAtras.set_sensitive(False)
		self.toolbuttonGenerarLiquidacion.set_sensitive(False)
		
		
	def llenar_prestamo_caja(self):
		detalle_cuotas=[]
		self.diccionario_caja=[]
		table=gtk.Table(1,5,True)
		sql	="""
			 SELECT nombre_caja_compensacion,
			 rut_trabajador,condicion,
			 valor_prestamo,cantidad_cuotas,
			 cuota_activa, detalle_cuotas
			 FROM prestamo_caja
			 WHERE rut_trabajador='%s'
			 ORDER BY codigo_prestamo
			 """%(self.rut_trabajador)
		self.cursor.execute(sql)
		c=self.cursor.fetchall()
		self.frame115.hide()
		if not (len(c)==0):
			self.alignment113.remove(self.vboxPrestamoCaja)
			self.vboxPrestamoCaja=gtk.VBox(False,0)
			self.alignment113.add(self.vboxPrestamoCaja)
			self.frame115.show_all()
			for a in range(len(c)):
				label1=gtk.Label()
				label1.set_markup("<b>Condicion</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(c[a][2]))
				frame.add(entrada)
				table.attach(frame,0,1,0,1)
				label1=gtk.Label()
				label1.set_markup("<b>Caja de Compensacion</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(c[a][0]))
				frame.add(entrada)
				table.attach(frame,1,2,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Numero de Cuota</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(c[a][5])+"/"+str(c[a][4]))
				frame.add(entrada)
				table.attach(frame,2,3,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Valor Cuota</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				detalle_cuotas=eval(str(c[a][6]))
				entrada.set_text(str(detalle_cuotas[c[a][5]][2]))
				frame.add(entrada)
				table.attach(frame,3,4,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Fecha de Vencimiento</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(detalle_cuotas[c[a][5]][1])
				frame.add(entrada)
				table.attach(frame,4,5,0,1)
				
				self.vboxPrestamoCaja.pack_start(table, False, True)
				table.show()
				self.vboxPrestamoCaja.show_all()
				table=gtk.Table(1,5,True)
				self.diccionario_caja.append([str(c[a][5])+"/"+str(c[a][4]),str(detalle_cuotas[c[a][5]][2]),str(c[a][0])])
			
	def llenar_prestamo_empleador(self):
		detalle_cuotas=[]
		self.diccionario_empresa=[]
		table=gtk.Table(1,3,True)
		sql	="""
			 SELECT detalle_cuotas,
			 cuota_activa, cantidad_cuotas
			 FROM prestamo_empresa
			 WHERE rut_trabajador='%s'
			 ORDER BY codigo_prestamo_empresa
			 """%(self.rut_trabajador) 
		self.cursor.execute(sql)
		c=self.cursor.fetchall()
		self.frame114.hide()
		if not (len(c)==0):
			self.alignment112.remove(self.vboxPrestamoEmpleador)
			self.vboxPrestamoEmpleador=gtk.VBox(False,0)
			self.alignment112.add(self.vboxPrestamoEmpleador)
			self.frame114.show_all()
			for a in range(len(c)):
				cadena=str(c[a][0])
				detalles=[]
				detalles=eval(cadena)
				label1=gtk.Label()
				label1.set_markup("<b>Numero de Cuota</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(c[a][1])+"/"+str(c[a][2]))
				frame.add(entrada)
				table.attach(frame,0,1,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Valor Cuota</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(detalles[c[a][1]][2]))
				frame.add(entrada)
				table.attach(frame,1,2,0,1)
				
				
				label1=gtk.Label()
				label1.set_markup("<b>Fecha de Vencimiento</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				detalle_cuotas=eval(str(c[a][1]))
				entrada.set_text(detalles[c[a][1]][1])
				frame.add(entrada)
				table.attach(frame,2,3,0,1)
				
				self.vboxPrestamoEmpleador.pack_start(table, False, True)
				table.show()
				self.vboxPrestamoEmpleador.show_all()
				table=gtk.Table(1,3,True)
				self.diccionario_empresa.append([str(c[a][1])+"/"+str(c[a][2]),str(detalles[c[a][1]][2])])
		
		
	def llenar_prestamo_fonasa(self):
		detalle_cuotas=[]
		self.diccionario_fonasa=[]
		table=gtk.Table(1,4,True)
		sql	="""
			 SELECT condicion,cuota_activa,detalle_cuotas,
			 cantidad_cuotas
			 FROM prestamo_salud
			 WHERE rut_trabajador='%s'
			 ORDER BY codigo_prestamo_salud
			 """%(self.rut_trabajador)
		self.cursor.execute(sql)
		c=self.cursor.fetchall()
		self.frame108.hide()
		if not (len(c)==0):
			self.alignment106.remove(self.vboxPrestamoSalud)
			self.vboxPrestamoSalud=gtk.VBox(False,0)
			self.alignment106.add(self.vboxPrestamoSalud)
			self.frame108.show_all()
			for a in range(len(c)):
				label1=gtk.Label()
				label1.set_markup("<b>Condicion</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(c[a][0]))
				frame.add(entrada)
				table.attach(frame,0,1,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Numero de Cuota</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(str(c[a][1])+"/"+str(c[a][3]))
				frame.add(entrada)
				table.attach(frame,1,2,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Valor Cuota</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				detalle_cuotas=eval(str(c[a][2]))
				entrada.set_text(str(detalle_cuotas[c[a][1]][2]))
				frame.add(entrada)
				table.attach(frame,2,3,0,1)
				
				label1=gtk.Label()
				label1.set_markup("<b>Fecha de Vencimiento</b>")
				label1.set_use_markup(True)
				frame=gtk.Frame()
				frame.set_label_widget(label1)	
				entrada=gtk.Entry(0)
				entrada.set_text(detalle_cuotas[c[a][1]][1])
				frame.add(entrada)
				table.attach(frame,3,4,0,1)
				
				self.vboxPrestamoSalud.pack_start(table, False, True)
				table.show()
				self.vboxPrestamoSalud.show_all()
				table=gtk.Table(1,4,True)
				self.diccionario_fonasa.append([str(c[a][1])+"/"+str(c[a][3]),str(detalle_cuotas[c[a][1]][2])])
		
	def llenar_otros_descuentos(self):
		detalle_cuotas=[]
		self.diccionario_otros_descuentos=[]
		sql	="""
			 SELECT d.nombre_descuento, s.detalle_descuento,
			 s.cuota_activa_descuento, s.numero_cuotas_descuento
			 FROM se_le_cargan s, descuento d
			 WHERE s.rut_trabajador='%s' AND
			 d.rut_empresa='%s' AND
			 s.codigo_descuento=d.codigo_descuento
			 ORDER BY s.codigo_descuento
			 """%(self.rut_trabajador, self.padre.rut_empresa_actual) 
		self.cursor.execute(sql)
		c=self.cursor.fetchall()
		self.frame116.hide()
		if not (len(c)==0):
			self.alignment114.remove(self.vboxOtrosDescuentos)
			self.vboxOtrosDescuentos=gtk.VBox(False,0)
			self.alignment114.add(self.vboxOtrosDescuentos)
			self.frame116.show_all()
			for a in range(len(c)):
				cadena=str(c[a][1])
				detalles=[]
				detalles=eval(cadena)
				if c[a][3]==1:
					table=gtk.Table(1,2,True)
					label1=gtk.Label()
					label1.set_markup("<b>Nombre descuento</b>")
					label1.set_use_markup(True)
					frame=gtk.Frame()
					frame.set_label_widget(label1)	
					entrada=gtk.Entry(0)
					entrada.set_text(str(c[a][0]))
					frame.add(entrada)
					table.attach(frame,0,1,0,1)
					
					label1=gtk.Label()
					label1.set_markup("<b>Valor</b>")
					label1.set_use_markup(True)
					frame=gtk.Frame()
					frame.set_label_widget(label1)	
					entrada=gtk.Entry(0)
					entrada.set_text(str(detalles[0][2]))
					frame.add(entrada)
					table.attach(frame,1,2,0,1)
					
					self.vboxOtrosDescuentos.pack_start(table, False, True)
					table.show()
					self.vboxOtrosDescuentos.show_all()
					self.diccionario_otros_descuentos.append([0,str(c[a][0]),str(detalles[0][2])])
				else:
					table=gtk.Table(1,4,True)
					label1=gtk.Label()
					label1.set_markup("<b>Nombre descuento</b>")
					label1.set_use_markup(True)
					frame=gtk.Frame()
					frame.set_label_widget(label1)	
					entrada=gtk.Entry(0)
					entrada.set_text(str(c[a][0]))
					frame.add(entrada)
					table.attach(frame,0,1,0,1)
					
					label1=gtk.Label()
					label1.set_markup("<b>Numero cuota</b>")
					label1.set_use_markup(True)
					frame=gtk.Frame()
					frame.set_label_widget(label1)	
					entrada=gtk.Entry(0)
					entrada.set_text(str(c[a][2])+"/"+str(c[a][3]))
					frame.add(entrada)
					table.attach(frame,1,2,0,1)

					label1=gtk.Label()
					label1.set_markup("<b>Valor Cuota</b>")
					label1.set_use_markup(True)
					frame=gtk.Frame()
					frame.set_label_widget(label1)	
					entrada=gtk.Entry(0)
					entrada.set_text(str(detalles[c[a][2]-1][2]))
					frame.add(entrada)
					table.attach(frame,2,3,0,1)
					
					label1=gtk.Label()
					label1.set_markup("<b>Fecha de Vencimiento</b>")
					label1.set_use_markup(True)
					frame=gtk.Frame()
					frame.set_label_widget(label1)	
					entrada=gtk.Entry(0)
					entrada.set_text(detalles[c[a][2]-1][1])
					frame.add(entrada)
					table.attach(frame,3,4,0,1)
					
					self.vboxOtrosDescuentos.pack_start(table, False, True)
					table.show()
					self.vboxOtrosDescuentos.show_all()
					self.diccionario_otros_descuentos.append([1,str(c[a][0]),str(c[a][2])+"/"+str(c[a][3]),str(detalles[c[a][2]-1][2])])
	
	
	def on_toolbuttonInicioVacaciones_clicked(self, toolCalendario=None):
		a=Calendario(3)
		a.padre=self.padre
		a.windowCalendario.show()
		
	def on_toolbuttonFinVacaciones_clicked(self, toolCalendario=None):
		a=Calendario(4)
		a.padre=self.padre
		a.windowCalendario.show()
	
	def on_entryInicioVacaciones_changed(self, entry=None):
		self.toolbuttonFinVacaciones.set_sensitive(True)
		if (self.padre.t_pl_antecedentesliquidacion.inicio_vacaciones_time<self.padre.t_pl_antecedentesliquidacion.fin_vacaciones_time):
			if not(self.fin_vacaciones_time==None):
				self.entryDiasVacaciones.set_text(str((int(time.strftime("%s",time.localtime(self.fin_vacaciones_time - self.inicio_vacaciones_time))))/86400))
		else:
			self.entryDiasVacaciones.set_text("0")
			
	def on_entryFinVacaciones_changed(self, entry=None):
		if (self.padre.t_pl_antecedentesliquidacion.inicio_vacaciones_time<self.padre.t_pl_antecedentesliquidacion.fin_vacaciones_time):
			self.entryDiasVacaciones.set_text(str((int(time.strftime("%s",time.localtime(self.fin_vacaciones_time - self.inicio_vacaciones_time))))/86400))
		else:
			self.entryDiasVacaciones.set_text("0")
			
	def on_entryInicioLicencia_changed(self, entry=None):
		self.toolbuttonFinLicencia.set_sensitive(True)
		if (self.padre.t_pl_antecedentesliquidacion.inicio_licencia_time<self.padre.t_pl_antecedentesliquidacion.fin_licencia_time):
			if not(self.fin_licencia_time==None):
				self.entryDiasLicencia.set_text(str((int(time.strftime("%s",time.localtime(self.fin_licencia_time - self.inicio_licencia_time))))/86400))
		else:
			self.entryDiasLicencia.set_text("0")
			
	def on_entryFinLicencia_changed(self, entry=None):
		if (self.padre.t_pl_antecedentesliquidacion.inicio_licencia_time<self.padre.t_pl_antecedentesliquidacion.fin_licencia_time):
			self.entryDiasLicencia.set_text(str((int(time.strftime("%s",time.localtime(self.fin_licencia_time - self.inicio_licencia_time))))/86400))
		else:
			self.entryDiasLicencia.set_text("0")
	
	def on_entryInicioPermiso_changed(self, entry=None):
		self.toolbuttonFinPermiso.set_sensitive(True)
		if (self.padre.t_pl_antecedentesliquidacion.inicio_permiso_time<self.padre.t_pl_antecedentesliquidacion.fin_permiso_time):
			if not(self.fin_permiso_time==None):
				self.entryDiasPermiso.set_text(str((int(time.strftime("%s",time.localtime(self.fin_permiso_time - self.inicio_permiso_time))))/86400))
		else:
			self.entryDiasPermiso.set_text("0")
			
	def on_entryFinPermiso_changed(self, entry=None):
		if (self.padre.t_pl_antecedentesliquidacion.inicio_permiso_time<self.padre.t_pl_antecedentesliquidacion.fin_permiso_time):
			self.entryDiasPermiso.set_text(str((int(time.strftime("%s",time.localtime(self.fin_permiso_time - self.inicio_permiso_time))))/86400))
		else:
			self.entryDiasPermiso.set_text("0")
						
						
	def on_entryDiasVacaciones_changed(self, entry=None):
		if not(self.entryInicioVacaciones.get_text()=="" and self.entryFinVacaciones.get_text()==""):
			if not (self.entryDiasLicencia.get_text()=="" and self.entryDiasPermiso.get_text()==""):
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasVacaciones.get_text()) - int(self.entryDiasLicencia.get_text()) - int(self.entryDiasPermiso.get_text())))
				return
			else:
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasVacaciones.get_text())))
				return 
			
			if not (self.entryDiasPermiso.get_text()==""):	
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasVacaciones.get_text()) - int(self.entryDiasPermiso.get_text())))
				return
				
			if not (self.entryDiasLicencia.get_text()==""):
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasVacaciones.get_text()) - int(self.entryDiasLicencia.get_text())))
				return
				
	def on_entryDiasLicencia_changed(self, entry=None):
		if not(self.entryInicioLicencia.get_text()=="" and self.entryFinLicencia.get_text()==""):
			if not (self.entryDiasVacaciones.get_text()=="" and self.entryDiasPermiso.get_text()==""):
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasVacaciones.get_text()) - int(self.entryDiasLicencia.get_text()) - int(self.entryDiasPermiso.get_text())))
				return
			else:
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasLicencia.get_text())))
				return
			
			if not (self.entryDiasPermiso.get_text()==""):	
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasLicencia.get_text()) - int(self.entryDiasPermiso_get_text())))
				return
				
			if not (self.entryDiasVacaciones.get_text()==""):
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasLicencia.get_text()) - int(self.entryDiasVacaciones.get_text())))
				return

	def on_entryDiasPermiso_changed(self, entry=None):
		if not(self.entryInicioPermiso.get_text()=="" and self.entryFinPermiso.get_text()==""):
			if not (self.entryDiasVacaciones.get_text()=="" and self.entryDiasLicencia.get_text()==""):
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasVacaciones.get_text()) - int(self.entryDiasLicencia.get_text()) - int(self.entryDiasPermiso.get_text())))
				return
			else:
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasPermiso.get_text())))
				return
			
			if not (self.entryDiasLicencia.get_text()==""):	
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasPermiso.get_text()) - int(self.entryDiasLicencia.get_text())))
				return
				
			if not (self.entryDiasVacaciones.get_text()==""):
				self.entryDiasTrabajados.set_text(str(30 - int(self.entryDiasPermiso.get_text()) - int(self.entryDiasVacaciones.get_text())))
				return

	def on_toolbuttonInicioLicencia_clicked(self, toolCalendario=None):
		a=Calendario(5)
		a.padre=self.padre
		a.windowCalendario.show()
	
	def on_toolbuttonFinLicencia_clicked(self, toolCalendario=None):
		a=Calendario(6)
		a.padre=self.padre
		a.windowCalendario.show()
	
	def on_toolbuttonInicioVacacionesNoImponibles_clicked(self, toolCalendario=None):
		a=Calendario(9)
		a.padre=self.padre
		a.windowCalendario.show()
		
	def on_toolbuttonFinVacacionesNoImponibles_clicked(self, toolCalendario=None):
		a=Calendario(10)
		a.padre=self.padre
		a.windowCalendario.show()
		
	def on_toolbuttonInicioPermiso_clicked(self, toolCalendario=None):
		a=Calendario(11)
		a.padre=self.padre
		a.windowCalendario.show()
		
	def on_toolbuttonFinPermiso_clicked(self, toolCalendario=None):
		a=Calendario(12)
		a.padre=self.padre
		a.windowCalendario.show()
		
	def on_toolbuttonAtras_clicked(self, toolbuttonAtras=None):
		self.padre.notebookMain.prev_page()

	def on_toolbuttonVueltas_clicked(self, toolbuttonVueltas=None):
		self.vueltas=ViajesRealizados(self.padre.cursor,self.padre.rut_empresa_actual, self.padre, self.rut_trabajador)
		self.vueltas.window1.show_all()
		self.padre.vbox1.set_sensitive(False)
	
	def on_toolbuttonAnticipos_clicked(self,toolbuttonAnticipo=None):
		self.anticipo_trabajador=Anticipos(self.cursor,self.padre,self.padre.t_pl_antecedentesliquidacion.rut_trabajador)
		self.anticipo_trabajador.window1.show()
		self.padre.vbox1.set_sensitive(False)
	
	def on_entryDiasTrabajados_changed(self, entry=None, cantidad=None):
		if not (self.tipo_trabajador=='ADMINISTRATIVO'):
			if cantidad==None:
				if not self.entryDiasTrabajados.get_text()=='':
					self.entryViaticos.set_text(str(int(self.entryDiasTrabajados.get_text())*1000))
			else:
				if not self.entryDiasTrabajados.get_text=='':
					self.entryViaticos.set_text(str(int(self.entryDiasTrabajados.get_text())*1000 -cantidad*1000))
		return

	def on_entryBonoViajes_changed(self,entry=None):
		if not (self.entryBonoViajes.get_text()=='' or self.entryBonoViajes.get_text()==None):
			sql="""SELECT porcentaje_afp
			FROM afp
			WHERE nombre_afp='%s'
			"""%(self.entryNombreAfp.get_text())
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			valor=r[0][0]*(int(self.entrySueldoBase.get_text())+int(self.entryBonoViajes.get_text()))
			self.entryCotizacionObligatoria.set_text(str(int(valor)))

			sql="""SELECT porcentaje_salud
			FROM salud
			WHERE nombre_salud='%s'
			"""%(self.entrySalud.get_text())
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			if self.entrySalud.get_text()=='FONASA':
				valor=r[0][0]*(int(self.entrySueldoBase.get_text())+int(self.entryBonoViajes.get_text()))
				self.entryDescuentoSalud.set_text(str(int(valor)))
			else:
				if not (self.padre.listatrabajadores.movimientopersonal.pactado_adicional==None or self.padre.listatrabajadores.movimientopersonal.pactado_adicional==0):
					sql="""SELECT uf
					FROM monto_factores_topes
					"""
					self.cursor.execute(sql)
					r=self.cursor.fetchall()
					self.entryDescuentoSalud.set_text(str(int(self.padre.listatrabajadores.movimientopersonal.pactado_adicional*r[0][0])))
				else:
					valor=r[0][0]*(int(self.entrySueldoBase.get_text())+int(self.entryBonoViajes.get_text()))
					self.entryDescuentoSalud.set_text(str(int(valor)))
		return
	
	def on_toolbuttonGenerarLiquidacion_clicked(self, toolbutton=None):
		total_haber=0
		total_imponible=0
		sub_total=0
		total_descuentos=0
		self.datos_liquidacion_sueldo["rut trabajador"]=(self.rut_trabajador)
		sql="""SELECT apellido_paterno_trabajador,
		apellido_materno_trabajador,
		nombres_trabajador
		FROM trabajador
		WHERE rut_trabajador='%s'
		"""%(self.rut_trabajador)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		self.datos_liquidacion_sueldo["nombre trabajador"]=(r[0][2]+" " +r[0][0]+" "+r[0][1])
		sql	="""SELECT fecha_proceso, codigo_proceso
				FROM proceso_remuneracion
				WHERE rut_empresa='%s' 
				AND estado_proceso='ABIERTO'  
			"""%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		self.codigo_proceso=r[0][1]
		self.datos_liquidacion_sueldo["fecha liquidacion"]=(r[0][0])
		self.datos_liquidacion_sueldo["dias trabajados"]=(self.entryDiasTrabajados.get_text())
		self.datos_liquidacion_sueldo["sueldo base"]=(self.entrySueldoBase.get_text())
		self.datos_liquidacion_sueldo["bono de viajes"]=(self.entryBonoViajes.get_text())
		total_imponible=int(self.entrySueldoBase.get_text())+int(self.entryBonoViajes.get_text())
		self.datos_liquidacion_sueldo["total imponible"]=(total_imponible)
		self.datos_liquidacion_sueldo["numero de cargas"]=(self.entryNumeroCargas.get_text())
		self.datos_liquidacion_sueldo["total cargas"]=(self.entryValorTotal.get_text())
		self.datos_liquidacion_sueldo["viatico"]=(self.entryViaticos.get_text())
		self.datos_liquidacion_sueldo["movilizacion"]=(self.entryMovilizacion.get_text())
		sub_total=int(self.entryValorTotal.get_text())+int(self.entryViaticos.get_text())+int(self.entryMovilizacion.get_text())
		self.datos_liquidacion_sueldo["sub total"]=(sub_total)
		total_haber=total_imponible+sub_total
		self.datos_liquidacion_sueldo["total haber"]=(total_haber)
		self.datos_liquidacion_sueldo["nombre afp"]=(self.entryNombreAfp.get_text())
		sql="""SELECT porcentaje_afp
		FROM afp
		WHERE nombre_afp='%s'
		"""%(self.entryNombreAfp.get_text())
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		self.datos_liquidacion_sueldo["porcentaje afp"]=(float(r[0][0]*100))
		self.datos_liquidacion_sueldo["cotizacion obligatoria"]=(self.entryCotizacionObligatoria.get_text())
		total_descuentos=int(self.entryCotizacionObligatoria.get_text())
		sql="""SELECT porcentaje_salud
		FROM salud
		WHERE nombre_salud='%s'
		"""%(self.entrySalud.get_text())
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		if self.entrySalud.get_text()=='FONASA':
			self.datos_liquidacion_sueldo["salud"]=(self.entrySalud.get_text())
			self.datos_liquidacion_sueldo["porcentaje salud"]=(float(r[0][0]*100))
			self.datos_liquidacion_sueldo["descuento salud"]=(self.entryDescuentoSalud.get_text())
		else:
			self.datos_liquidacion_sueldo["salud"]=(self.entrySalud.get_text())
			if not (self.padre.listatrabajadores.movimientopersonal.pactado_adicional==None or self.padre.listatrabajadores.movimientopersonal.pactado_adicional==0):
				sql="""SELECT uf
				FROM monto_factores_topes
				"""
				self.cursor.execute(sql)
				uf=self.cursor.fetchall()
				self.datos_liquidacion_sueldo["cantidad uf"]=(self.padre.listatrabajadores.movimientopersonal.pactado_adicional)
				self.datos_liquidacion_sueldo["valor uf"]=(uf[0][0])
				self.datos_liquidacion_sueldo["adicional pactado"]=(self.entryDescuentoSalud.get_text())
			else:
				self.datos_liquidacion_sueldo["porcentaje salud"]=(int(r[0][0]*100))
				self.datos_liquidacion_sueldo["descuento salud"]=(self.entryDescuentoSalud.get_text())
		total_descuentos=total_descuentos+int(self.entryDescuentoSalud.get_text())
		if self.entryOptaSeguroCesantia.get_text()=='SI':
			self.datos_liquidacion_sueldo["porcentaje seguro cesantia"]=(int(float(self.entryPorcientroSeguroDesempleo.get_text())*100))
			self.datos_liquidacion_sueldo["valor seguro cesantia"]=(int(total_imponible*float(self.entryPorcientroSeguroDesempleo.get_text())))
			total_descuentos=total_descuentos+int(total_imponible*float(self.entryPorcientroSeguroDesempleo.get_text()))
		if not (self.entryAhorroVoluntario.get_text()=='0' or self.entryAhorroVoluntario.get_text()==""):
			self.datos_liquidacion_sueldo["ahorro voluntario"]=(self.entryAhorroVoluntario.get_text())
			total_descuentos=total_descuentos++int(self.entryAhorroVoluntario.get_text())
		total_prestamos=0
		if not len(self.diccionario_caja)==0:
			self.datos_liquidacion_sueldo["caja compensacion"]=(self.diccionario_caja[0][2])
			self.datos_liquidacion_sueldo["prestamo caja cuota"]=(self.diccionario_caja[0][0])
			self.datos_liquidacion_sueldo["prestamo caja valor cuota"]=(self.diccionario_caja[0][1])
			total_prestamos=int(self.diccionario_caja[0][1])
			total_descuentos=total_descuentos+int(self.diccionario_caja[0][1])
		if not self.entryCompaniaSeguroVidaPosee.get_text()=='NO':
			self.datos_liquidacion_sueldo["compania de seguro"]=(self.entryCompania.get_text())
			self.datos_liquidacion_sueldo["seguro de vida cuota"]=(self.entryNumeroCuotaCompania.get_text())
			self.datos_liquidacion_sueldo["seguro de vida valor cuota"]=(self.entryValorCompania.get_text())
			total_descuentos=total_descuentos+int(self.entryValorCompania.get_text())
		if not self.entryRutCodigoInterno.get_text()=="":
			self.datos_liquidacion_sueldo["leasing cuota"]=(self.entryNumeroCuota.get_text())
			self.datos_liquidacion_sueldo["leasing valor cuota"]=(self.entryAporteDinero.get_text())
			total_descuentos=total_descuentos+int(self.entryAporteDinero.get_text())
		if not len(self.diccionario_empresa)==0:
			self.datos_liquidacion_sueldo["prestamo empresa cuota"]=(self.diccionario_empresa[0][0])
			self.datos_liquidacion_sueldo["prestamo empresa valor cuota"]=(self.diccionario_empresa[0][1])
			total_prestamos=total_prestamos+int(self.diccionario_empresa[0][1])
			total_descuentos=total_descuentos+int(self.diccionario_empresa[0][1])
		if not len(self.diccionario_fonasa)==0:
			self.datos_liquidacion_sueldo["prestamo fonasa cuota"]=(self.diccionario_fonasa[0][0])
			self.datos_liquidacion_sueldo["prestamo fonasa valor cuota"]=(self.diccionario_fonasa[0][1])
			total_prestamos=total_prestamos+int(self.diccionario_fonasa[0][1])
			total_descuentos=total_descuentos+int(self.diccionario_fonasa[0][1])
		if not len(self.diccionario_otros_descuentos)==0:
			self.datos_liquidacion_sueldo["otros descuentos"]=(self.diccionario_otros_descuentos[0][1])
			self.datos_liquidacion_sueldo["otros descuentos valor cuota"]=(self.diccionario_otros_descuentos[0][2])
			total_descuentos=total_descuentos+int(self.diccionario_otros_descuentos[0][2])
		
		self.datos_liquidacion_sueldo["total descuentos"]=(total_descuentos)
		self.datos_liquidacion_sueldo["vales o anticipos"]=(self.entryAnticipos.get_text())		
		
		#guarda vueltas
		texto='[]'
		if not (self.modelo_vueltas==None):
			aux=[]
			iterador= self.modelo_vueltas.get_iter_first()
			while not iterador==None:
				aux.append([self.modelo_vueltas.get_value(iterador,0),self.modelo_vueltas.get_value(iterador,1),self.modelo_vueltas.get_value(iterador,2), self.modelo_vueltas.get_value(iterador,3)])
				iterador= self.modelo_vueltas.iter_next(iterador)
			texto='[' +", ".join(["['%s', '%s', '%s', '%s']" %(n1,n2,n3,n4) for n1,n2,n3,n4 in aux])+']'
		print texto
		self.datos_liquidacion_sueldo["detalle_vueltas"]=(eval(texto))
		
		self.pdf=Liquidacion_pdf(self.datos_liquidacion_sueldo,self.padre)
		self.pdf.Abre_pdf("LIQUIDACION_SUELDO_%s_%s_%s.pdf"%(self.datos_liquidacion_sueldo["fecha liquidacion"].strftime("%B").upper(),
															 self.datos_liquidacion_sueldo["fecha liquidacion"].strftime("%Y"),
															 self.datos_liquidacion_sueldo["nombre trabajador"]))
		
		archivo=file("LIQUIDACION_SUELDO_%s_%s_%s.pdf"%(self.datos_liquidacion_sueldo["fecha liquidacion"].strftime("%B").upper(),
															 self.datos_liquidacion_sueldo["fecha liquidacion"].strftime("%Y"),
															 self.datos_liquidacion_sueldo["nombre trabajador"]),"rb").read()
		archivo=PgSQL.PgBytea(archivo)

		sql	="""SELECT codigo_historico_liquidacion
		FROM historico_liquidacion
		WHERE rut_trabajador='%s'
		and codigo_proceso='%s'
		"""%(self.rut_trabajador, self.codigo_proceso)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
				
		if len(r)==0:
			if not self.datos_liquidacion_sueldo.has_key("adicional pactado"):
				descuento_salud=self.datos_liquidacion_sueldo["descuento salud"]
			else:
				descuento_salud=self.datos_liquidacion_sueldo["adicional pactado"]

			self.cursor.execute("""INSERT INTO historico_liquidacion
			(rut_trabajador, 
			codigo_proceso,
			liquidacion_sueldo,
			historico_sueldo_base,
			historico_bono_viajes,
			historico_total_remuneracion_im,
			historico_numero_cargas,
			historico_valor_cargas,
			historico_movilizacion,
			historico_viaticos,
			historico_total_haber,
			historico_organismo_previsional,
			historico_cotizacion_previsiona,
			historico_organismo_salud,
			historico_descuento_salud,
			historico_total_prestamos,
			historico_total_otros,
			historico_total_descuentos,
			historico_alcance_liquido,
			historico_anticipos,
			historico_saldo_liquido,
			historico_gtk_model)
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
			self.rut_trabajador, 
			self.codigo_proceso, 
			archivo,
			self.datos_liquidacion_sueldo["sueldo base"],
			self.datos_liquidacion_sueldo["bono de viajes"],
			self.datos_liquidacion_sueldo["total imponible"],
			self.datos_liquidacion_sueldo["numero de cargas"],
			self.datos_liquidacion_sueldo["total cargas"],
			self.datos_liquidacion_sueldo["movilizacion"],
			self.datos_liquidacion_sueldo["viatico"],
			self.datos_liquidacion_sueldo["total haber"],
			self.datos_liquidacion_sueldo["nombre afp"],
			self.datos_liquidacion_sueldo["cotizacion obligatoria"],
			self.datos_liquidacion_sueldo["salud"],
			descuento_salud,
			total_prestamos,
			total_descuentos-total_prestamos,
			total_descuentos,
			int(self.datos_liquidacion_sueldo["total imponible"])-total_descuentos,
			self.datos_liquidacion_sueldo["vales o anticipos"],
			int(self.datos_liquidacion_sueldo["total imponible"])-total_descuentos-int(self.datos_liquidacion_sueldo["vales o anticipos"]),
			texto)
			self.padre.cnx.commit()
		else:
			if not self.datos_liquidacion_sueldo.has_key("adicional pactado"):
				descuento_salud=self.datos_liquidacion_sueldo["descuento salud"]
			else:
				descuento_salud=self.datos_liquidacion_sueldo["adicional pactado"]
			
			self.cursor.execute(""" UPDATE historico_liquidacion
				 SET 
				 liquidacion_sueldo=%s,
				 historico_sueldo_base=%s,
				 historico_bono_viajes=%s,
				 historico_total_remuneracion_im=%s,
				 historico_numero_cargas=%s,
				 historico_valor_cargas=%s,
				 historico_movilizacion=%s,
				 historico_viaticos=%s,
				 historico_total_haber=%s,
				 historico_organismo_previsional=%s,
				 historico_cotizacion_previsiona=%s,
				 historico_organismo_salud=%s,
				 historico_descuento_salud=%s,
				 historico_total_prestamos=%s,
				 historico_total_otros=%s,
				 historico_total_descuentos=%s,
				 historico_alcance_liquido=%s,
				 historico_anticipos=%s,
				 historico_saldo_liquido=%s,
				 historico_gtk_model=%s
				 WHERE rut_trabajador=%s
				 and codigo_proceso=%s
				 """, 
				 archivo,
				 self.datos_liquidacion_sueldo["sueldo base"],
				 self.datos_liquidacion_sueldo["bono de viajes"],
				 self.datos_liquidacion_sueldo["total imponible"],
				 self.datos_liquidacion_sueldo["numero de cargas"],
				 self.datos_liquidacion_sueldo["total cargas"],
				 self.datos_liquidacion_sueldo["movilizacion"],
				 self.datos_liquidacion_sueldo["viatico"],
				 self.datos_liquidacion_sueldo["total haber"],
				 self.datos_liquidacion_sueldo["nombre afp"],
				 self.datos_liquidacion_sueldo["cotizacion obligatoria"],
				 self.datos_liquidacion_sueldo["salud"],
				 descuento_salud,
				 total_prestamos,
				 total_descuentos-total_prestamos,
				 total_descuentos,
				 int(self.datos_liquidacion_sueldo["total imponible"])-total_descuentos,
				 self.datos_liquidacion_sueldo["vales o anticipos"],
				 int(self.datos_liquidacion_sueldo["total imponible"])-total_descuentos-int(self.datos_liquidacion_sueldo["vales o anticipos"]),
				 texto,
				 self.rut_trabajador,
				 self.codigo_proceso)
		
		#marcar a trabajador como procesado
		sql	="""UPDATE trabaja
		SET
		procesado='%s'
		WHERE rut_trabajador='%s'
		and rut_empresa='%s'
		"""%(1,self.rut_trabajador, self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		self.padre.cnx.commit()
		
		self.padre.listatrabajadores.lista_datos_No_Procesados()
		self.padre.listatrabajadores.lista_datos_Procesados()
		
		#sql="""SELECT liquidacion_sueldo 
		#FROM historico_liquidacion
		#WHERE rut_trabajador='%s'
		#"""%(self.rut_trabajador)
		#self.cursor.execute(sql)
		#r=self.cursor.fetchall()
		#archivo=r[0][0].value
		#file("liquidacion.pdf","wb").write(archivo)	
		#self.pdf.Abre_pdf("liquidacion.pdf")
		
		self.padre.notebookMain.prev_page()
		
		return
