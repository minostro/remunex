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
import calendar

class DescuentoTrabajador(GladeConnect):
	def __init__(self, cursor,rut_trabajador,padre):
		GladeConnect.__init__(self, "glade/descuento_trabajador.glade")
		self.cursor=cursor
		self.padre=padre
		self.detalles=[]
		self.rut_trabajador=rut_trabajador
		self.pk_descuento=None
		self.sensibilidad_objetos(0)
		#botones de menu
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#metodo para los comboboxentry caja compensacion
		self.crear_combos_modelo_descuento()
		self.llenar_combos_descuento()
		#metodo para treeview detalles
		self.define_vista_detalles()
		self.crea_modelo_detalles()
		#metodo para treeview detalles
		self.define_vista_descuento()
		self.crea_modelo_descuento()
		self.lista_datos_descuento()
		
	def sensibilidad_objetos(self, marca):
		if marca==0:
			self.spinbuttonCantidad.set_sensitive(False)
			self.comboboxentryDescuento.set_sensitive(False)
			self.comboboxentryDescuento.child.set_sensitive(False)
			self.entryValorDescuento.set_sensitive(False)
			self.spinbuttonCantidadCuotas.set_sensitive(False)
			self.entryFechaInicio.set_sensitive(False)
			self.entryFechaTermino.set_sensitive(False)
			self.toolbuttonFechaInicio.set_sensitive(False)
			return
		if marca==1:
			self.comboboxentryDescuento.set_sensitive(True)
			self.spinbuttonCantidadCuotas.set_sensitive(True)
			self.spinbuttonCantidad.set_sensitive(True)
			self.entryFechaInicio.set_sensitive(True)
			self.toolbuttonFechaInicio.set_sensitive(True)
			return

	def texto_objetos(self):
		self.comboboxentryDescuento.child.set_text("")
		self.entryValorDescuento.set_text("")
		self.spinbuttonCantidadCuotas.set_text("1")
		self.spinbuttonCantidad.set_text("1")
		self.entryFechaInicio.set_text("")
		self.entryFechaTermino.set_text("")
		return
		
	def on_toolbuttonNuevo_clicked(self, toolbutton=None):
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.sensibilidad_objetos(1)
		self.texto_objetos()
		self.comboboxentryDescuento.grab_focus()
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
		descuento=[]
		descuento.append(self.rut_trabajador.upper())
		descuento.append(self.pk_descuento)
		descuento.append(self.entryFechaInicio.get_text())
		descuento.append(self.spinbuttonCantidadCuotas.get_text())
		descuento.append('{'+cadena+'}')
		descuento.append(self.entryFechaTermino.get_text())
		descuento.append(int(self.spinbuttonCantidadCuotas.get_text())*int(self.entryValorDescuento.get_text()))
		descuento.append(1)
		try:
			sql	="""
				 INSERT INTO se_le_cargan
				 (rut_trabajador,codigo_descuento,
				 fecha_inicio_descuento,numero_cuotas_descuento,
				 detalle_descuento,fecha_termino_descuento,
				 valor_descuento, cuota_activa_descuento
				 )
				 VALUES ("""+ ",".join(["'%s'" %(n1) for n1 in descuento])+")"
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.lista_datos_descuento()
			self.on_toolbuttonNuevo_clicked()
		except:
			print sys.exc_info()[1]	

	def on_toolbuttonCerrar_clicked(self, toolbutton=None):
		self.window1.hide()

	def llenar_combos_descuento(self):
		self.modelo_caja.clear()
		sql	="""
			 SELECT codigo_descuento, nombre_descuento,
			 valor_descuento
			 FROM descuento
			 WHERE rut_empresa='%s'
			 ORDER BY codigo_descuento
			 """%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		self.r=self.cursor.fetchall()
		if not len(self.r)==0:
			for i in self.r:
				self.modelo_caja.append([i[1]])
		else:
			print "no existen descuentos"
			
	def crear_combos_modelo_descuento(self):
		self.modelo_caja= gtk.ListStore(str) 
		self.comboboxentryDescuento.set_model(self.modelo_caja)
		cell=gtk.CellRendererText()
		self.comboboxentryDescuento.pack_start(cell,True)
		self.comboboxentryDescuento.add_attribute(cell,'text',0)
		return
		
	def on_comboboxentryDescuento_changed(self,combo=None):
		model_aux = self.comboboxentryDescuento.get_model()
		active = self.comboboxentryDescuento.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryDescuento.child.set_text(elemento)
		self.entryValorDescuento.set_text(str(self.r[active][2]))
		self.pk_descuento=self.r[active][0]
		return

	def on_toolbuttonFechaInicio_clicked(self, toolbutton=None):
		a=Calendario(14)
		a.padre=self.padre
		a.windowCalendario.show()
		

	def on_spinbuttonCantidad_changed(self,spin=None):
		if self.spinbuttonCantidad.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.comboboxentryDescuento.child.get_text()==""):
			if not (self.entryValorDescuento.get_text()==""):
				if not (self.spinbuttonCantidadCuotas.get_text()==""):
					if not (self.entryFechaInicio.get_text()==""):
						self.lista_datos_detalles()
						return
		self.modelo_detalles.clear()
		return

	def on_entryValorDescuento_changed(self, entry=None):
		if self.entryValorDescuento.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.spinbuttonCantidad.get_text()==""):
			if not (self.entryValorDescuento.get_text()==""):
				if not (self.spinbuttonCantidadCuotas.get_text()==""):
					if not (self.entryFechaInicio.get_text()==""):
						self.lista_datos_detalles()
						return
		self.modelo_detalles.clear()
		return
	
	def on_spinbuttonCantidadCuotas_value_changed(self,spin=None):
		if self.spinbuttonCantidadCuotas.get_text()=="":
			self.modelo_detalles.clear()
			return

		if not (self.comboboxentryDescuento.child.get_text()==""):
			if not (self.entryValorDescuento.get_text()==""):
				if not (self.spinbuttonCantidad.get_text()==""):
					if not (self.entryFechaInicio.get_text()==""):
						self.lista_datos_detalles()
						return
		self.modelo_detalles.clear()
		return

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
		cuota_fija=(int(self.spinbuttonCantidad.get_text())*int(self.entryValorDescuento.get_text()))/int(self.spinbuttonCantidadCuotas.get_text())
		for i in range (int(self.spinbuttonCantidadCuotas.get_text())-1):
			tiempo=time.mktime((self.padre.anio, self.padre.mes+i, self.padre.dia, 0, 0, 0, 0, 0, -1))
			anio = time.strftime("%Y",time.localtime(tiempo))			
			mes = time.strftime("%m",time.localtime(tiempo))
			dia = calendar.monthrange(int(anio),int(mes))[1]
			self.modelo_detalles.append([str(i+1),"%s-%s-%s"%(anio,mes,dia),cuota_fija])
		ultimo_cuota=(int(self.spinbuttonCantidad.get_text())*int(self.entryValorDescuento.get_text()))-cuota_fija*(int(self.spinbuttonCantidadCuotas.get_text())-1)
		tiempo=time.mktime((self.padre.anio, self.padre.mes+int(self.spinbuttonCantidadCuotas.get_text())-1, self.padre.dia, 0, 0, 0, 0, 0, -1))
		anio = time.strftime("%Y",time.localtime(tiempo))			
		mes = time.strftime("%m",time.localtime(tiempo))
		dia = calendar.monthrange(int(anio),int(mes))[1]
		self.modelo_detalles.append([int(self.spinbuttonCantidadCuotas.get_text()),"%s-%s-%s"%(anio,mes,dia),ultimo_cuota])
		self.entryFechaTermino.set_text("%s-%s-%s"%(anio,mes,dia))
		return
		

	def define_vista_descuento(self):
		
		lbl = unicode('Codigo descuento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewDescuento.append_column(column)
		
		lbl = unicode('Nombre descuento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewDescuento.append_column(column)
		
		lbl = unicode('Fecha inicio')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewDescuento.append_column(column)
		
		lbl = unicode('Fecha termino')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewDescuento.append_column(column)
		
		lbl = unicode('Valor descuento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=4)
		self.treeviewDescuento.append_column(column)

				
	def crea_modelo_descuento(self):
		self.modelo = gtk.ListStore(str, str, str, str, str)
		self.treeviewDescuento.set_model(self.modelo)
		
	def lista_datos_descuento(self):
		self.modelo.clear()
		sql	="""SELECT s.codigo_se_le_cargan,d.nombre_descuento,
		s.fecha_inicio_descuento,s.fecha_termino_descuento,
		s.valor_descuento 
		FROM se_le_cargan s, descuento d 
		WHERE s.codigo_descuento=d.codigo_descuento AND
		s.rut_trabajador='%s' AND d.rut_empresa='%s'
		ORDER BY s.codigo_descuento
		"""%(self.rut_trabajador,self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if not len(r)==0:
			for i in r:
				self.modelo.append([i[0],i[1],i[2].strftime("%Y-%m-%d"),i[3].strftime("%Y-%m-%d"),i[4]])
		return
