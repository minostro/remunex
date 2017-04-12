#!/usr/bin/env python
  
############################################################################
#    Copyright (C) 2005 by												   #
#                                                                          #
#        Milton Inostroza Aguilera         						           #
#           minoztro@gmail.com                					           #
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
import gobject
import time
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
from conexionbd import *

class Calendario(GladeConnect):
	"Crea, Modifica, Actualiza las Afp's"
	
	def __init__(self,tipo):
		GladeConnect.__init__(self, "glade/calendario.glade")
		self.ventana_activa = None
		self.padre = None
		self.marca=1
		self.tipo=tipo
		self.anio=None
		self.mes=None
		self.dia=None
		self.entryFechaProceso.set_sensitive(False)
		
		
	def on_calendar1_day_selected_double_click(self, widget):
		self.anio, self.mes, self.dia =self.calendar1.get_date()
		self.mes=self.mes+1
		if not self.mes/10:
			self.mes="0"+str(self.mes)
		
		cadena="%s-%s-%s"%(self.anio,self.mes,self.dia)
		self.mes=int(self.mes)
		
		self.padre.anio=self.anio
		self.padre.mes=self.mes
		self.padre.dia=self.dia

		
		if self.tipo==0:
			self.padre.fecha_proceso=cadena
			self.padre.fecha_actual=time.strftime("%Y-%m-%d", time.localtime())			
			self.padre.windowMain.set_sensitive(True)
			self.windowCalendario.hide()
			return
			
		if self.tipo==1:
			self.padre.ingresarseleccionar.entryFechaNacimiento.set_text(cadena)
			self.windowCalendario.hide()
			return
		
		if self.tipo==2:
			self.padre.antecedentespersonales.entryFechaIngreso.set_text(cadena)
			self.windowCalendario.hide()
			return 
		
		if self.tipo==3:
			self.padre.t_pl_antecedentesliquidacion.inicio_vacaciones_time=time.mktime((self.anio, self.mes+1, self.dia, 0, 0, 0, 0, 0, -1))
			if not (self.padre.t_pl_antecedentesliquidacion.inicio_vacaciones_time<self.padre.t_pl_antecedentesliquidacion.fin_vacaciones_time):
				self.padre.t_pl_antecedentesliquidacion.entryInicioVacaciones.set_text(cadena)
				self.padre.t_pl_antecedentesliquidacion.entryFinVacaciones.set_text("")
			else:
				self.padre.t_pl_antecedentesliquidacion.entryInicioVacaciones.set_text(cadena)
				self.padre.t_pl_antecedentesliquidacion.entryDiasVacaciones.set_text("0")
			self.windowCalendario.hide()
			return
			
		if self.tipo==4:
			self.padre.t_pl_antecedentesliquidacion.fin_vacaciones_time=time.mktime((self.anio, self.mes+1, self.dia, 0, 0, 0, 0, 0, -1))
			if (self.padre.t_pl_antecedentesliquidacion.inicio_vacaciones_time<self.padre.t_pl_antecedentesliquidacion.fin_vacaciones_time):
				self.padre.t_pl_antecedentesliquidacion.entryFinVacaciones.set_text(cadena)
			else:
				self.padre.t_pl_antecedentesliquidacion.entryFinVacaciones.set_text("")
			self.windowCalendario.hide()
			self.padre.t_pl_antecedentesliquidacion.toolbuttonFinVacaciones.set_sensitive(True)
			return
		
		if self.tipo==5:
			self.padre.t_pl_antecedentesliquidacion.inicio_licencia_time=time.mktime((self.anio, self.mes+1, self.dia, 0, 0, 0, 0, 0, -1))
			if not (self.padre.t_pl_antecedentesliquidacion.inicio_licencia_time<self.padre.t_pl_antecedentesliquidacion.fin_licencia_time):
				self.padre.t_pl_antecedentesliquidacion.entryInicioLicencia.set_text(cadena)
				self.padre.t_pl_antecedentesliquidacion.entryFinLicencia.set_text("")
			else:
				self.padre.t_pl_antecedentesliquidacion.entryInicioLicencia.set_text(cadena)
			self.windowCalendario.hide()
			return
		
		if self.tipo==6:
			self.padre.t_pl_antecedentesliquidacion.fin_licencia_time=time.mktime((self.anio, self.mes+1, self.dia, 0, 0, 0, 0, 0, -1))
			if (self.padre.t_pl_antecedentesliquidacion.inicio_licencia_time<self.padre.t_pl_antecedentesliquidacion.fin_licencia_time):
				self.padre.t_pl_antecedentesliquidacion.entryFinLicencia.set_text(cadena)
			else:
				self.padre.t_pl_antecedentesliquidacion.entryFinLicencia.set_text("")
				self.padre.t_pl_antecedentesliquidacion.fin_licencia_time=0
			self.windowCalendario.hide()
			self.padre.t_pl_antecedentesliquidacion.toolbuttonFinLicencia.set_sensitive(True)
			return
		
		if self.tipo==7:
			self.padre.antecedentesliquidacion.prestamocaja.entryFechaInicio.set_text(cadena)
			if not self.padre.antecedentesliquidacion.prestamocaja.spinbuttonCantidadCuotas.get_text()=="":
				if not (self.padre.antecedentesliquidacion.prestamocaja.comboboxentryCondicion.child.get_text()==""):
					if not (self.padre.antecedentesliquidacion.prestamocaja.entryCodigoPrestamo.get_text()==""):
						if not (self.padre.antecedentesliquidacion.prestamocaja.entryMontoOtorgado.get_text()==""):
							if not (self.padre.antecedentesliquidacion.prestamocaja.entryUltimoDividendo.get_text()==""):
								if not (self.padre.antecedentesliquidacion.prestamocaja.entryPrimerDividendo.get_text()==""):
									mytime = time.mktime((self.anio, self.mes+int(self.padre.antecedentesliquidacion.prestamocaja.spinbuttonCantidadCuotas.get_text()), self.dia, 0, 0, 0, 0, 0, -1))
									self.padre.antecedentesliquidacion.prestamocaja.entryFechaTermino.set_text(time.strftime("%Y-%m-%d",time.localtime(mytime)))
									self.windowCalendario.hide()
									self.padre.antecedentesliquidacion.prestamocaja.lista_datos_detalles()
									return
			self.padre.antecedentesliquidacion.prestamocaja.entryFechaTermino.set_text("")
			self.padre.antecedentesliquidacion.prestamocaja.modelo_detalles.clear()
			self.windowCalendario.hide()
			return
		
		if self.tipo==8:
			self.padre.antecedentesliquidacion.prestamoempresa.entryFechaInicio.set_text(cadena)
			if not self.padre.antecedentesliquidacion.prestamoempresa.spinbuttonCantidadCuotas.get_text()=="":
				if not self.padre.antecedentesliquidacion.prestamoempresa.entryValorPrestamo.get_text()=="":
					mytime = time.mktime((self.anio, self.mes+int(self.padre.antecedentesliquidacion.prestamoempresa.spinbuttonCantidadCuotas.get_text()), self.dia, 0, 0, 0, 0, 0, -1))
					self.padre.antecedentesliquidacion.prestamoempresa.entryFechaTermino.set_text(time.strftime("%Y-%m-%d",time.localtime(mytime)))
					self.windowCalendario.hide()
					self.padre.antecedentesliquidacion.prestamoempresa.lista_datos_detalles()
					return
			self.padre.antecedentesliquidacion.prestamoempresa.entryFechaTermino.set_text("")
			self.windowCalendario.hide()
		
		if self.tipo==9:
			self.padre.t_pl_antecedentesliquidacion.entryInicioVacacionesNoImponibles.set_text(cadena)
			self.windowCalendario.hide()
			return

		if self.tipo==10:
			self.padre.t_pl_antecedentesliquidacion.entryFinVacacionesNoImponibles.set_text(cadena)
			self.windowCalendario.hide()
			return
			
		if self.tipo==11:
			self.padre.t_pl_antecedentesliquidacion.inicio_permiso_time=time.mktime((self.anio, self.mes+1, self.dia, 0, 0, 0, 0, 0, -1))
			if not (self.padre.t_pl_antecedentesliquidacion.inicio_permiso_time<self.padre.t_pl_antecedentesliquidacion.fin_permiso_time):
				self.padre.t_pl_antecedentesliquidacion.entryInicioPermiso.set_text(cadena)
				self.padre.t_pl_antecedentesliquidacion.entryFinPermiso.set_text("")
			else:
				self.padre.t_pl_antecedentesliquidacion.entryInicioPermiso.set_text(cadena)
			self.windowCalendario.hide()
			return 

		if self.tipo==12:
			self.padre.t_pl_antecedentesliquidacion.fin_permiso_time=time.mktime((self.anio, self.mes+1, self.dia, 0, 0, 0, 0, 0, -1))
			if (self.padre.t_pl_antecedentesliquidacion.inicio_permiso_time<self.padre.t_pl_antecedentesliquidacion.fin_permiso_time):
				self.padre.t_pl_antecedentesliquidacion.entryFinPermiso.set_text(cadena)
			else:
				self.padre.t_pl_antecedentesliquidacion.entryFinPermiso.set_text("")
				self.padre.t_pl_antecedentesliquidacion.fin_permiso_time=0
			self.windowCalendario.hide()
			self.padre.t_pl_antecedentesliquidacion.toolbuttonFfonasainPermiso.set_sensitive(True)
			return
			
		if self.tipo==13:
			self.padre.antecedentesliquidacion.prestamofonasa.entryFechaInicio.set_text(cadena)
			if not self.padre.antecedentesliquidacion.prestamofonasa.spinbuttonCantidadCuotas.get_text()=="":
				mytime = time.mktime((self.anio, self.mes+int(self.padre.antecedentesliquidacion.prestamofonasa.spinbuttonCantidadCuotas.get_text()), self.dia, 0, 0, 0, 0, 0, -1))
				self.padre.antecedentesliquidacion.prestamofonasa.entryFechaTermino.set_text(time.strftime("%Y-%m-%d",time.localtime(mytime)))
				self.windowCalendario.hide()
				self.padre.antecedentesliquidacion.prestamofonasa.lista_datos_detalles()
				return
			else:
				self.padre.antecedentesliquidacion.prestamofonasa.entryFechaTermino.set_text("")
				self.windowCalendario.hide()
		if self.tipo==14:
			self.padre.antecedentesliquidacion.descuento_trabajador.entryFechaInicio.set_text(cadena)
			if not self.padre.antecedentesliquidacion.descuento_trabajador.spinbuttonCantidadCuotas.get_text()=="":
				mytime = time.mktime((self.anio, self.mes+int(self.padre.antecedentesliquidacion.descuento_trabajador.spinbuttonCantidadCuotas.get_text()), self.dia, 0, 0, 0, 0, 0, -1))
				self.padre.antecedentesliquidacion.descuento_trabajador.entryFechaTermino.set_text(time.strftime("%Y-%m-%d",time.localtime(mytime)))
				self.windowCalendario.hide()
				self.padre.antecedentesliquidacion.descuento_trabajador.lista_datos_detalles()
				return
			else:
				self.padre.antecedentesliquidacion.descuento_trabajador.entryFechaTermino.set_text("")
				self.windowCalendario.hide()
