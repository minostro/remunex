#!/usr/bin/env python

############################################################################
#    Copyright (C) 2005 by												   #
#                                                                          #
#        Milton Inostroza Aguilera        						           #
#           minoztro@gmail.com              					           #
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
import gobject
from pyPgSQL.PgSQL import connect
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
import sys
from dialogo_error import DialogoError
from types import StringType


class ViajesRealizados(GladeConnect):
	
	def __init__(self,cursor,rut_empresa_actual,padre, rut_trabajador):
		GladeConnect.__init__(self, "glade/viajes_realizados.glade")
		self.cursor=cursor
		self.padre = padre
		self.pk_direccion = None
		self.rut_empresa_actual=rut_empresa_actual
		self.rut_trabajador=rut_trabajador
		#poniendo no editable a las cajas 
		self.comboboxentryVuelta.set_sensitive(True)
		self.comboboxentryVuelta.child.set_sensitive(False)
		self.entryCantidad.set_sensitive(True)
		self.entryValorUnitario.set_sensitive(False)
		self.entryValorTotal.set_sensitive(False)
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		#pone el foco en codigo
		self.comboboxentryVuelta.grab_focus()
		#metodo para treeview
		self.define_vista()
		self.crea_modelo()
		#self.lista_datos()
		#crear comboboxentryVuelta
		self.crear_combo_modelo_vuelta()
		self.llenar_combo_vuelta()
		
	def llenar_valor_vueltas(self):
		iterador= self.modelo.get_iter_first()
		suma=0
		while not iterador==None:
			suma=suma+int(self.modelo.get_value(iterador,3))
			iterador= self.modelo.iter_next(iterador)
		self.padre.t_pl_antecedentesliquidacion.entryBonoViajes.set_text(str(suma))
		return	
	
	def cantidad_vueltas_bolivia(self):
		iterador= self.modelo.get_iter_first()
		suma=0
		while not iterador==None:
			auxiliar=self.modelo.get_value(iterador,1).split("-")
			if ("BOLIVIA" in auxiliar):
				suma=suma+int(self.modelo.get_value(iterador,0))
			iterador= self.modelo.iter_next(iterador)
		self.padre.t_pl_antecedentesliquidacion.on_entryDiasTrabajados_changed(None,suma)
		return	
		
	def llenar_combo_vuelta(self):
		self.modelo_vuelta.clear()
		
		sql="""SELECT nombre_vuelta, valor_vuelta_chofer,
		valor_vuelta_auxiliar
		FROM vuelta
		ORDER BY nombre_vuelta
		"""
		self.cursor.execute(sql)
		self.vueltas=self.cursor.fetchall()
		for i in self.vueltas:
			self.modelo_vuelta.append([i[0]])
	
	def crear_combo_modelo_vuelta(self):
		self.modelo_vuelta= gtk.ListStore(str) 
		self.comboboxentryVuelta.set_model(self.modelo_vuelta)
		cell=gtk.CellRendererText()
		self.comboboxentryVuelta.pack_start(cell,True)
		self.comboboxentryVuelta.add_attribute(cell,'text',0)
		return

	def on_comboboxentryVuelta_changed(self,combo=None):
		model_aux = self.comboboxentryVuelta.get_model()
		active = self.comboboxentryVuelta.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryVuelta.child.set_text(elemento)
		if self.padre.t_pl_antecedentesliquidacion.tipo_trabajador=="CONDUCTOR DE BUS":
			self.entryValorUnitario.set_text(str(self.vueltas[active][1]))
		elif self.padre.t_pl_antecedentesliquidacion.tipo_trabajador=="AUXILIAR DE BUS":
			self.entryValorUnitario.set_text(str(self.vueltas[active][2]))
		return

	def define_vista(self):
		lbl = unicode('Cantidad')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewVueltasRealizadas.append_column(column)
		lbl = unicode('Vuelta')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewVueltasRealizadas.append_column(column)
		lbl = unicode('Valor Unitario $')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewVueltasRealizadas.append_column(column)
		lbl = unicode('Valor Total $')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewVueltasRealizadas.append_column(column)
		

	def crea_modelo(self):
		if self.padre.t_pl_antecedentesliquidacion.modelo_vueltas==None:
			self.modelo = gtk.ListStore(str,str,str,str)
			self.treeviewVueltasRealizadas.set_model(self.modelo)
		else:
			self.modelo=self.padre.t_pl_antecedentesliquidacion.modelo_vueltas
			self.treeviewVueltasRealizadas.set_model(self.modelo)
		return
		
	def lista_datos(self):
		self.modelo.clear()
		
		sql="""SELECT v.nombre_vuelta, 
		v.valor_vuelta
		FROM vuelta v, ofrece o
		WHERE v.nombre_vuelta=o.nombre_vuelta 
		ORDER BY v.nombre_vuelta
		"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()

		for i in r:
			self.modelo.append(i)
		return

	
	def on_treeviewVueltasRealizadas_row_activated(self, tree, row, column):
		self.iterador = self.modelo.get_iter(row)
		self.comboboxentryVuelta.child.set_text(self.modelo[row][1])
		self.entryValorUnitario.set_text(self.modelo[row][2])
		self.entryCantidad.set_text(self.modelo[row][0])
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(True)
		#poniendo editable a las cajas 
		self.comboboxentryVuelta.set_sensitive(False)
		self.entryCantidad.set_sensitive(True)
		self.entryValorTotal.set_sensitive(False)
		#foco en codigo
		self.entryCantidad.grab_focus()

	
	def on_toolbuttonNuevo_clicked(self, toolbuttonNuevo=None):
		#Poniendo editable a las cajas 
		self.comboboxentryVuelta.set_sensitive(True)
		self.entryCantidad.set_sensitive(True)
		self.entryValorTotal.set_sensitive(False)
		#BORRA EL CONTENIDO DE LAS CAJAS DE TEXTO
		self.comboboxentryVuelta.child.set_text("")
		self.entryCantidad.set_text("")
		self.entryValorTotal.set_text("")
		self.entryValorUnitario.set_text("")
		#Deja sensible a anadir
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(False)
		#foco en origen
		self.comboboxentryVuelta.grab_focus()
		return
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadir=None):
		if (self.entryCantidad.get_text()==""):
			return
			
		datos=[]
		datos.append(self.entryCantidad.get_text())
		datos.append(self.comboboxentryVuelta.child.get_text())
		datos.append(self.entryValorUnitario.get_text())
		datos.append(self.entryValorTotal.get_text())
		self.modelo.append(datos)
		self.on_toolbuttonNuevo_clicked()
		return
		
	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizar=None):
		if self.comboboxentryVuelta.child.get_text()=="" or self.entryCantidad.get_text()=="" or self.entryValorTotal.get_text()=="":
			self.on_toolbuttonNuevo_clicked()
			return
		self.modelo.set(self.iterador, 0,self.entryCantidad.get_text(),1,self.comboboxentryVuelta.child.get_text(),2,self.entryValorUnitario.get_text(),3,self.entryValorTotal.get_text())
		self.on_toolbuttonNuevo_clicked()
	
	def on_toolbuttonQuitar_clicked(self, toolbuttonQuitar=None):
		treeiter = self.modelo.remove(self.iterador)
		self.on_toolbuttonNuevo_clicked()
		return
		
	def on_window1_delete_event(self, Widget=None, Event=None):
		self.padre.vbox1.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.modelo_vueltas=self.modelo
		self.llenar_valor_vueltas()
		self.cantidad_vueltas_bolivia()
		self.window1.destroy()
		return False
	
	def on_toolbuttonCerrar_clicked(self, toolbuttonCerrar=None):
		self.padre.vbox1.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.modelo_vueltas=self.modelo
		self.llenar_valor_vueltas()
		self.cantidad_vueltas_bolivia()
		self.window1.destroy()
		return
		
	def on_entryCantidad_changed(self, entryCantidad=None):
		if not (self.entryCantidad.get_text()=="" or self.comboboxentryVuelta.child.get_text()==""):
			aux=int(self.entryValorUnitario.get_text())
			aux2=int(self.entryCantidad.get_text())
			self.entryValorTotal.set_text(str(aux*aux2))
		else:
			self.entryValorTotal.set_text("")
			self.entryCantidad.set_text("")
		return
