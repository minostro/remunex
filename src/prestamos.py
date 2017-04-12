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
import gobject
import sys
import time

from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
from calendario import *
import time
import calendar
from dialogo_error import DialogoError
from types import StringType

class PrestamoCajaCompensacion(GladeConnect):
	def __init__(self, cursor,rut_trabajador,padre):
		GladeConnect.__init__(self, "glade/prestamocajacompensacion.glade")
		self.cursor=cursor
		self.padre=padre
		self.detalles=[]
		self.rut_trabajador=rut_trabajador
		self.objetos_sensitive(0)
		self.toolbuttonFechaInicio.set_sensitive(False)
		#botones de menu
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#metodo para los comboboxentry caja compensacion
		self.llenar_caja()
		#metodo para treeview detalles
		self.define_vista_detalles()
		self.crea_modelo_detalles()
		#metodo para treeview detalles
		self.define_vista_prestamo()
		self.crea_modelo_prestamo()
		self.lista_datos_prestamo()
	
	def objetos_sensitive(self,marca):
		if marca==0:
			self.entryNombreCajaCompensacion.set_sensitive(False)
			self.comboboxentryCondicion.set_sensitive(False)
			self.comboboxentryCondicion.child.set_sensitive(False)
			self.entryCodigoPrestamo.set_sensitive(False)
			self.entryMontoOtorgado.set_sensitive(False)
			self.spinbuttonCantidadCuotas.set_sensitive(False)
			self.entryPrimerDividendo.set_sensitive(False)
			self.entryUltimoDividendo.set_sensitive(False)
			self.entryFechaInicio.set_sensitive(False)
			self.entryFechaTermino.set_sensitive(False)
			return		
		else:
			self.comboboxentryCondicion.set_sensitive(True)
			self.entryCodigoPrestamo.set_sensitive(True)
			self.entryMontoOtorgado.set_sensitive(True)
			self.spinbuttonCantidadCuotas.set_sensitive(True)
			self.entryPrimerDividendo.set_sensitive(True)
			self.entryUltimoDividendo.set_sensitive(True)
			self.toolbuttonFechaInicio.set_sensitive(True)
			return
	

	def on_toolbuttonNuevo_clicked(self, toolbutton=None):
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.objetos_sensitive(1)
		self.comboboxentryCondicion.child.set_text("")
		self.entryCodigoPrestamo.set_text("")
		self.entryMontoOtorgado.set_text("")
		self.spinbuttonCantidadCuotas.set_text("1")
		self.entryPrimerDividendo.set_text("")
		self.entryUltimoDividendo.set_text("")
		self.entryFechaInicio.set_text("")
		self.entryFechaTermino.set_text("")
		self.entryCodigoPrestamo.grab_focus()
		self.modelo_detalles.clear()
		
	def on_toolbuttonAnadir_clicked(self, toolbutton=None):
		model=self.treeviewDetalleCuotas.get_model()	
		iterador= model.get_iter_first()
		lista=[]
		while not iterador==None:
			lista.append(model.get_value(iterador,0))
			lista.append(model.get_value(iterador,1))
			lista.append(model.get_value(iterador,2))
			iterador= model.iter_next(iterador)
		cadena=",".join(["{%s,%s,%s}"%(lista[i],lista[i+1],lista[i+2]) for i in xrange(0,len(lista),3)])
		
		prestamocaja=[]
		prestamocaja.append(self.entryCodigoPrestamo.get_text().upper())
		prestamocaja.append(self.padre.rut_empresa_actual)
		prestamocaja.append(self.entryNombreCajaCompensacion.get_text())
		prestamocaja.append(self.rut_trabajador.upper())
		prestamocaja.append(self.comboboxentryCondicion.child.get_text())
		prestamocaja.append(self.entryMontoOtorgado.get_text())
		prestamocaja.append(self.spinbuttonCantidadCuotas.get_text())
		prestamocaja.append(self.entryFechaInicio.get_text())
		prestamocaja.append(self.entryFechaTermino.get_text())
		prestamocaja.append('{'+cadena+'}')
		prestamocaja.append(1)
		
		try:
			sql	="""
				 INSERT INTO prestamo_caja
				 (codigo_prestamo,rut_empresa,
				  nombre_caja_compensacion,
				  rut_trabajador,condicion,valor_prestamo,
				  cantidad_cuotas,
				  fecha_inicio_prestamo,fecha_termino_prestamo,
				  detalle_cuotas, cuota_activa
				 )
				 VALUES ("""+ ",".join(["'%s'" %(n1) for n1 in prestamocaja])+")"
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.lista_datos_prestamo()
			self.on_toolbuttonNuevo_clicked()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
	"""
	def on_toolbuttonActualizar_clicked(self, toolbutton=None):
	def on_toolbuttonQuitar_clicked(self, toolbutton=None):
	"""
	def on_toolbuttonCerrar_clicked(self, toolbutton=None):
		self.windowPrestamoCaja.hide()

	def llenar_caja(self):
		sql	="""
			 SELECT nombre_caja_compensacion
			 FROM empleador
			 WHERE rut_empresa='%s'
			 """%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		self.entryNombreCajaCompensacion.set_text(r[0][0])
			

	def on_toolbuttonFechaInicio_clicked(self, toolbutton=None):
		a=Calendario(7)
		a.padre=self.padre
		a.windowCalendario.show()
		
		
	def define_vista_detalles(self):
		
		lbl = unicode('Numero Cuota')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewDetalleCuotas.append_column(column)
		
		lbl = unicode('Fecha Vencimiento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewDetalleCuotas.append_column(column)
		
		lbl = unicode('Valor Cuota')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewDetalleCuotas.append_column(column)
				
	def crea_modelo_detalles(self):
		self.modelo_detalles = gtk.ListStore(str, str, str)
		self.treeviewDetalleCuotas.set_model(self.modelo_detalles)
		
	def lista_datos_detalles(self):
		self.modelo_detalles.clear()
		for i in range (int(self.spinbuttonCantidadCuotas.get_text())-1):
			tiempo=time.mktime((self.padre.anio, self.padre.mes+i, self.padre.dia, 0, 0, 0, 0, 0, -1))
			anio = time.strftime("%Y",time.localtime(tiempo))			
			mes = time.strftime("%m",time.localtime(tiempo))
			dia = calendar.monthrange(int(anio),int(mes))[1]
			self.modelo_detalles.append([str(i+1),"%s-%s-%s"%(anio,mes,dia),self.entryPrimerDividendo.get_text()])
		tiempo=time.mktime((self.padre.anio, self.padre.mes+int(self.spinbuttonCantidadCuotas.get_text())-1, self.padre.dia, 0, 0, 0, 0, 0, -1))
		anio = time.strftime("%Y",time.localtime(tiempo))			
		mes = time.strftime("%m",time.localtime(tiempo))
		dia = calendar.monthrange(int(anio),int(mes))[1]
		self.modelo_detalles.append([int(self.spinbuttonCantidadCuotas.get_text()),"%s-%s-%s"%(anio,mes,dia),self.entryUltimoDividendo.get_text()])
		self.entryFechaTermino.set_text("%s-%s-%s"%(anio,mes,dia))
		return
	
	
	def define_vista_prestamo(self):
		
		lbl = unicode('Codigo prestamo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewPrestamoCaja.append_column(column)
		
		lbl = unicode('Fecha inicio')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewPrestamoCaja.append_column(column)
		
		lbl = unicode('Fecha termino')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewPrestamoCaja.append_column(column)
		
		lbl = unicode('Valor prestamo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewPrestamoCaja.append_column(column)

				
	def crea_modelo_prestamo(self):
		self.modelo = gtk.ListStore(str, str, str, str)
		self.treeviewPrestamoCaja.set_model(self.modelo)
		
	def lista_datos_prestamo(self):
		self.modelo.clear()
		sql	="""
			 SELECT codigo_prestamo,fecha_inicio_prestamo,
			 fecha_termino_prestamo,valor_prestamo
			 FROM prestamo_caja WHERE rut_trabajador='%s'
			 ORDER BY codigo_prestamo
			 """%(self.rut_trabajador)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append([i[0],i[1].strftime("%Y-%m-%d"),i[2].strftime("%Y-%m-%d"),i[3]])
		return
		
	def on_spinbuttonCantidadCuotas_value_changed(self,alog=None):
		if self.spinbuttonCantidadCuotas.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.comboboxentryCondicion.child.get_text()==""):
			if not (self.entryCodigoPrestamo.get_text()==""):
				if not (self.entryMontoOtorgado.get_text()==""):
					if not (self.entryPrimerDividendo.get_text()==""):
						if not (self.entryUltimoDividendo.get_text()==""):
							if not (self.entryFechaInicio.get_text()==""):
								self.lista_datos_detalles()
								return
		self.modelo_detalles.clear()
		return
	
	def on_entryPrimerDividendo_changed(self, boton=None):
		if self.entryPrimerDividendo.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.comboboxentryCondicion.child.get_text()==""):
			if not (self.entryCodigoPrestamo.get_text()==""):
				if not (self.entryMontoOtorgado.get_text()==""):
					if not (self.spinbuttonCantidadCuotas.get_text()==""):
						if not (self.entryUltimoDividendo.get_text()==""):
							if not (self.entryFechaInicio.get_text()==""):
								self.lista_datos_detalles()
								return
		self.modelo_detalles.clear()
		return
		
	def on_entryUltimoDividendo_changed(self, boton=None):
		if self.entryUltimoDividendo.get_text()=="":
			self.modelo_detalles.clear()
			return
		
		if not (self.comboboxentryCondicion.child.get_text()==""):
			if not (self.entryCodigoPrestamo.get_text()==""):
				if not (self.entryMontoOtorgado.get_text()==""):
					if not (self.spinbuttonCantidadCuotas.get_text()==""):
						if not (self.entryPrimerDividendo.get_text()==""):
							if not (self.entryFechaInicio.get_text()==""):
								self.lista_datos_detalles()
								return
		self.modelo_detalles.clear()
		return


class PrestamoEmpresa(GladeConnect):
	def __init__(self, cursor,rut_trabajador):
		GladeConnect.__init__(self, "glade/prestamoempresa.glade")
		self.cursor=cursor
		self.padre=None
		self.detalles=[]
		self.rut_trabajador=rut_trabajador
		self.entryValorPrestamo.set_sensitive(False)
		self.spinbuttonCantidadCuotas.set_sensitive(False)
		self.entryFechaInicio.set_sensitive(False)
		self.entryFechaTermino.set_sensitive(False)
		self.toolbuttonFechaInicio.set_sensitive(False)
		#botones de menu
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#metodo para treeview detalles
		self.define_vista_detalles()
		self.crea_modelo_detalles()
		#metodo para treeview detalles
		self.define_vista_prestamo()
		self.crea_modelo_prestamo()
		self.lista_datos_prestamo()
		#foco
		self.entryValorPrestamo.grab_focus()

	def define_vista_detalles(self):
		
		lbl = unicode('Numero Cuota')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewDetalleCuotas.append_column(column)
		
		lbl = unicode('Fecha Vencimiento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewDetalleCuotas.append_column(column)
		
		lbl = unicode('Valor Cuota')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewDetalleCuotas.append_column(column)
				
	def crea_modelo_detalles(self):
		self.modelo_detalles = gtk.ListStore(str, str, str)
		self.treeviewDetalleCuotas.set_model(self.modelo_detalles)
		
	def lista_datos_detalles(self):
		self.modelo_detalles.clear()
		cuota_fija=int(self.entryValorPrestamo.get_text())/int(self.spinbuttonCantidadCuotas.get_text())
		for i in range (int(self.spinbuttonCantidadCuotas.get_text())-1):
			tiempo=time.mktime((self.padre.anio, self.padre.mes+i, self.padre.dia, 0, 0, 0, 0, 0, -1))
			anio = time.strftime("%Y",time.localtime(tiempo))			
			mes = time.strftime("%m",time.localtime(tiempo))
			dia = calendar.monthrange(int(anio),int(mes))[1]
			self.modelo_detalles.append([str(i+1),"%s-%s-%s"%(anio,mes,dia),cuota_fija])
		ultimo_cuota=int(self.entryValorPrestamo.get_text())-cuota_fija*(int(self.spinbuttonCantidadCuotas.get_text())-1)
		tiempo=time.mktime((self.padre.anio, self.padre.mes+int(self.spinbuttonCantidadCuotas.get_text())-1, self.padre.dia, 0, 0, 0, 0, 0, -1))
		anio = time.strftime("%Y",time.localtime(tiempo))			
		mes = time.strftime("%m",time.localtime(tiempo))
		dia = calendar.monthrange(int(anio),int(mes))[1]
		self.modelo_detalles.append([int(self.spinbuttonCantidadCuotas.get_text()),"%s-%s-%s"%(anio,mes,dia),ultimo_cuota])
		self.entryFechaTermino.set_text("%s-%s-%s"%(anio,mes,dia))
		return

	def define_vista_prestamo(self):
		lbl = unicode('Codigo prestamo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewPrestamoEmpresa.append_column(column)
		
		lbl = unicode('Fecha inicio')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewPrestamoEmpresa.append_column(column)
		
		lbl = unicode('Fecha termino')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewPrestamoEmpresa.append_column(column)
		
		lbl = unicode('Valor prestamo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewPrestamoEmpresa.append_column(column)

				
	def crea_modelo_prestamo(self):
		self.modelo = gtk.ListStore(str, str, str, str)
		self.treeviewPrestamoEmpresa.set_model(self.modelo)
		
	def lista_datos_prestamo(self):
		self.modelo.clear()
		sql	="""
			 SELECT codigo_prestamo_empresa,fecha_inicio_prestamo,
			 fecha_termino_prestamo,valor_prestamo
			 FROM prestamo_empresa WHERE rut_trabajador='%s'
			 ORDER BY codigo_prestamo_empresa
			 """%(self.rut_trabajador)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append([i[0],i[1].strftime("%Y-%m-%d"),i[2].strftime("%Y-%m-%d"),i[3]])
		return

	def on_toolbuttonNuevo_clicked(self, toolbutton=None):
		self.entryValorPrestamo.set_sensitive(True)
		self.spinbuttonCantidadCuotas.set_sensitive(True)
		self.toolbuttonFechaInicio.set_sensitive(True)
		self.entryValorPrestamo.set_text("")
		self.spinbuttonCantidadCuotas.set_text("1")
		self.entryFechaInicio.set_text("")
		self.entryFechaTermino.set_text("")
		self.entryValorPrestamo.grab_focus()
		self.modelo_detalles.clear()
		
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)

	def on_toolbuttonAnadir_clicked(self, toolbutton=None):
		model=self.treeviewDetalleCuotas.get_model()	
		iterador= model.get_iter_first()
		lista=[]
		while not iterador==None:
			lista.append(model.get_value(iterador,0))
			lista.append(model.get_value(iterador,1))
			lista.append(model.get_value(iterador,2))
			iterador= model.iter_next(iterador)
		cadena=",".join(["{%s,%s,%s}"%(lista[i],lista[i+1],lista[i+2]) for i in xrange(0,len(lista),3)])
		
		prestamoempresa=[]
		prestamoempresa.append(self.rut_trabajador.upper())
		prestamoempresa.append(self.padre.rut_empresa_actual)
		prestamoempresa.append(self.entryValorPrestamo.get_text())
		prestamoempresa.append(self.spinbuttonCantidadCuotas.get_text())
		prestamoempresa.append(self.entryFechaInicio.get_text())
		prestamoempresa.append(self.entryFechaTermino.get_text())
		prestamoempresa.append('{'+cadena+'}')
		prestamoempresa.append(1)
		
		try:
			sql	="""
				 INSERT INTO prestamo_empresa
				 (rut_trabajador, rut_empresa, valor_prestamo,
				  cantidad_cuotas,fecha_inicio_prestamo,
				  fecha_termino_prestamo,detalle_cuotas, 
				  cuota_activa)
				 VALUES ("""+ ",".join(["'%s'" %(n1) for n1 in prestamoempresa])+")"
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.lista_datos_prestamo()
			self.on_toolbuttonNuevo_clicked()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
		
		
	def on_toolbuttonCerrar_clicked(self, toolbutton=None):
		self.window1.hide()
		
	def on_toolbuttonFechaInicio_clicked(self, toolbutton=None):
		a=Calendario(8)
		a.padre=self.padre
		a.windowCalendario.show()


	def on_spinbuttonCantidadCuotas_value_changed(self,alog=None):
		if self.spinbuttonCantidadCuotas.get_text()=="":
			self.modelo_detalles.clear()
			return
		if not (self.entryValorPrestamo.get_text()==""):
			if not (self.entryFechaInicio.get_text()==""):
				self.lista_datos_detalles()
				return
		self.modelo_detalles.clear()
		return

	def on_entryValorPrestamo_changed(self, entry=None):
		if self.entryValorPrestamo.get_text()=="":
			self.modelo_detalles.clear()
			return
		if not (self.spinbuttonCantidadCuotas.get_text()==""):
			if not (self.entryFechaInicio.get_text()==""):
				self.lista_datos_detalles()
				return
		self.modelo_detalles.clear()
		return



class PrestamoFonasa(GladeConnect):
	def __init__(self, cursor,rut_trabajador):
		GladeConnect.__init__(self, "glade/prestamofonasa.glade")
		self.cursor=cursor
		self.padre=None
		self.rut_trabajador=rut_trabajador
		self.detalles=[]
		self.objetos_sensitive(0)
		self.toolbuttonFechaInicio.set_sensitive(False)
		#botones de menu
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#metodo para treeview detalles
		self.define_vista_detalles()
		self.crea_modelo_detalles()
		#metodo para treeview detalles
		self.define_vista_prestamo()
		self.crea_modelo_prestamo()
		self.lista_datos_prestamo()
		#foco
		self.entryMontoOtorgado.grab_focus()
	
	def objetos_sensitive(self,marca):
		if marca==0:
			self.comboboxentryCondicion.set_sensitive(False)
			self.comboboxentryCondicion.child.set_sensitive(False)
			self.entryCodigoPrestamo.set_sensitive(False)
			self.entryMontoOtorgado.set_sensitive(False)
			self.spinbuttonCantidadCuotas.set_sensitive(False)
			self.entryPrimerDividendo.set_sensitive(False)
			self.entryUltimoDividendo.set_sensitive(False)
			self.entryFechaInicio.set_sensitive(False)
			self.entryFechaTermino.set_sensitive(False)
			return		
		else:
			self.comboboxentryCondicion.set_sensitive(True)
			self.entryCodigoPrestamo.set_sensitive(True)
			self.entryMontoOtorgado.set_sensitive(True)
			self.spinbuttonCantidadCuotas.set_sensitive(True)
			self.entryPrimerDividendo.set_sensitive(True)
			self.entryUltimoDividendo.set_sensitive(True)
			self.toolbuttonFechaInicio.set_sensitive(True)
			return
	
	def on_toolbuttonNuevo_clicked(self, toolbutton=None):
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.objetos_sensitive(1)
		self.comboboxentryCondicion.child.set_text("")
		self.entryCodigoPrestamo.set_text("")
		self.entryMontoOtorgado.set_text("")
		self.spinbuttonCantidadCuotas.set_text("1")
		self.entryFechaInicio.set_text("")
		self.entryFechaTermino.set_text("")
		self.entryCodigoPrestamo.grab_focus()
		self.modelo_detalles.clear()
		
		
		
	def define_vista_detalles(self):
		
		lbl = unicode('Numero Cuota')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewDetalleCuotas.append_column(column)
		
		lbl = unicode('Fecha Vencimiento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewDetalleCuotas.append_column(column)
		
		lbl = unicode('Valor Cuota')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewDetalleCuotas.append_column(column)
				
	def crea_modelo_detalles(self):
		self.modelo_detalles = gtk.ListStore(str, str, str)
		self.treeviewDetalleCuotas.set_model(self.modelo_detalles)
		
	def lista_datos_detalles(self):
		self.modelo_detalles.clear()
		for i in range (int(self.spinbuttonCantidadCuotas.get_text())-1):
			tiempo=time.mktime((self.padre.anio, self.padre.mes+i, self.padre.dia, 0, 0, 0, 0, 0, -1))
			anio = time.strftime("%Y",time.localtime(tiempo))			
			mes = time.strftime("%m",time.localtime(tiempo))
			dia = calendar.monthrange(int(anio),int(mes))[1]
			self.modelo_detalles.append([str(i+1),"%s-%s-%s"%(anio,mes,dia),self.entryPrimerDividendo.get_text()])
		tiempo=time.mktime((self.padre.anio, self.padre.mes+int(self.spinbuttonCantidadCuotas.get_text())-1, self.padre.dia, 0, 0, 0, 0, 0, -1))
		anio = time.strftime("%Y",time.localtime(tiempo))			
		mes = time.strftime("%m",time.localtime(tiempo))
		dia = calendar.monthrange(int(anio),int(mes))[1]
		self.modelo_detalles.append([int(self.spinbuttonCantidadCuotas.get_text()),"%s-%s-%s"%(anio,mes,dia),self.entryUltimoDividendo.get_text()])
		self.entryFechaTermino.set_text("%s-%s-%s"%(anio,mes,dia))
		return

	def define_vista_prestamo(self):
		
		lbl = unicode('Codigo prestamo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewPrestamoFonasa.append_column(column)
		
		lbl = unicode('Fecha inicio')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewPrestamoFonasa.append_column(column)
		
		lbl = unicode('Fecha termino')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewPrestamoFonasa.append_column(column)
		
		lbl = unicode('Valor prestamo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewPrestamoFonasa.append_column(column)

				
	def crea_modelo_prestamo(self):
		self.modelo = gtk.ListStore(str, str, str, str)
		self.treeviewPrestamoFonasa.set_model(self.modelo)
		
	def lista_datos_prestamo(self):
		self.modelo.clear()
		sql	="""
			 SELECT codigo_prestamo_salud,fecha_inicio_prestamo,
			 fecha_termino_prestamo,valor_prestamo
			 FROM prestamo_salud WHERE rut_trabajador='%s'
			 ORDER BY codigo_prestamo_salud
			 """%(self.rut_trabajador)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append([i[0],i[1].strftime("%Y-%m-%d"),i[2].strftime("%Y-%m-%d"),i[3]])
		return
		
	def on_toolbuttonCerrar_clicked(self, toolbutton=None):
		self.windowPrestamoFonasa.destroy()
	
	def on_spinbuttonCantidadCuotas_value_changed(self,alog=None):
		if self.spinbuttonCantidadCuotas.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.comboboxentryCondicion.child.get_text()==""):
			if not (self.entryCodigoPrestamo.get_text()==""):
				if not (self.entryMontoOtorgado.get_text()==""):
					if not (self.entryPrimerDividendo.get_text()==""):
						if not (self.entryUltimoDividendo.get_text()==""):
							if not (self.entryFechaInicio.get_text()==""):
								self.lista_datos_detalles()
								return
		self.modelo_detalles.clear()
		return
	
	def on_entryPrimerDividendo_changed(self, boton=None):
		if self.entryPrimerDividendo.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.comboboxentryCondicion.child.get_text()==""):
			if not (self.entryCodigoPrestamo.get_text()==""):
				if not (self.entryMontoOtorgado.get_text()==""):
					if not (self.spinbuttonCantidadCuotas.get_text()==""):
						if not (self.entryUltimoDividendo.get_text()==""):
							if not (self.entryFechaInicio.get_text()==""):
								self.lista_datos_detalles()
								return
		self.modelo_detalles.clear()
		return
		
	def on_entryUltimoDividendo_changed(self, boton=None):
		if self.entryUltimoDividendo.get_text()=="":
			self.modelo_detalles.clear()
			return
		
		if not (self.comboboxentryCondicion.child.get_text()==""):
			if not (self.entryCodigoPrestamo.get_text()==""):
				if not (self.entryMontoOtorgado.get_text()==""):
					if not (self.spinbuttonCantidadCuotas.get_text()==""):
						if not (self.entryPrimerDividendo.get_text()==""):
							if not (self.entryFechaInicio.get_text()==""):
								self.lista_datos_detalles()
								return
		self.modelo_detalles.clear()
		return

	def on_toolbuttonFechaInicio_clicked(self, toolbutton=None):
		a=Calendario(13)
		a.padre=self.padre
		a.windowCalendario.show()

	def on_toolbuttonAnadir_clicked(self, toolbutton=None):
		model=self.treeviewDetalleCuotas.get_model()	
		iterador= model.get_iter_first()
		lista=[]
		while not iterador==None:
			lista.append(model.get_value(iterador,0))
			lista.append(model.get_value(iterador,1))
			lista.append(model.get_value(iterador,2))
			iterador= model.iter_next(iterador)
		cadena=",".join(["{%s,%s,%s}"%(lista[i],lista[i+1],lista[i+2]) for i in xrange(0,len(lista),3)])
		prestamofonasa=[]
		prestamofonasa.append(self.entryCodigoPrestamo.get_text().upper())
		prestamofonasa.append(self.padre.rut_empresa_actual)
		prestamofonasa.append(self.rut_trabajador.upper())
		prestamofonasa.append(self.comboboxentryCondicion.child.get_text())
		prestamofonasa.append(self.entryMontoOtorgado.get_text())
		prestamofonasa.append(self.spinbuttonCantidadCuotas.get_text())
		prestamofonasa.append(self.entryFechaInicio.get_text())
		prestamofonasa.append(self.entryFechaTermino.get_text())
		prestamofonasa.append('{'+cadena+'}')
		prestamofonasa.append(1)
		
		try:
			sql	="""
				 INSERT INTO prestamo_salud
				 (codigo_prestamo_salud, rut_empresa,rut_trabajador, 
				 condicion, valor_prestamo,cantidad_cuotas,
				 fecha_inicio_prestamo,fecha_termino_prestamo,
				 detalle_cuotas, cuota_activa)
				 VALUES ("""+ ",".join(["'%s'" %(n1) for n1 in prestamofonasa])+")"
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.lista_datos_prestamo()
			self.on_toolbuttonNuevo_clicked()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
