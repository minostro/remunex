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
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
from t_pl_movimientopersonal import MovimientoPersonal


class ListaTrabajadores(GladeConnect):
	"Lista a Los trabajadores de la Empresa "
	
	def __init__ (self,cursor, rut_empresa_actual):
		GladeConnect.__init__(self, "glade/t_pl_listatrabajadores.glade")
		self.cursor=cursor
		self.rut_empresa_actual=rut_empresa_actual
		self.ventana_activa = None
		self.padre = None
		self.rut_trabajador=None
		#poniendo no editable a las cajas 
		self.entryNombreEmpresa.set_sensitive(False)
		self.toolbuttonAdelante.set_sensitive(False)
		#poniendo valor a caja
		
		sql="""SELECT razon_social
			   FROM empleador
			   WHERE rut_empresa='%s'
			"""%(self.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		self.entryNombreEmpresa.set_text(r[0][0])
		
		#poniendo foco
		self.treeviewTrabajadoresNoProcesados.grab_focus()
		
		#metodo para treeview
		self.define_vista_No_Procesados()
		self.crea_modelo_No_Procesados()
		self.lista_datos_No_Procesados()
		
		self.define_vista_Procesados()
		self.crea_modelo_Procesados()
		self.lista_datos_Procesados()
		
	def define_vista_No_Procesados(self):
		lbl = unicode('R.U.T. Trabajador')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewTrabajadoresNoProcesados.append_column(column)
		lbl = unicode('Trabajador')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewTrabajadoresNoProcesados.append_column(column)
		

	def crea_modelo_No_Procesados(self):
		self.modelo = gtk.ListStore(str, str)
		self.treeviewTrabajadoresNoProcesados.set_model(self.modelo)

	def lista_datos_No_Procesados(self):
		self.modelo.clear()
		devolucion=[]
		devolucion.append("trabajador.rut_trabajador")
		devolucion.append("trabajador.nombres_trabajador")
		devolucion.append("trabajador.apellido_paterno_trabajador")
		devolucion.append("trabajador.apellido_materno_trabajador")
		
		
		sql="""SELECT t.rut_trabajador, t.nombres_trabajador,
			   t.apellido_paterno_trabajador, t. apellido_materno_trabajador
			   FROM trabajador t, trabaja
			   WHERE trabaja.rut_trabajador=t.rut_trabajador and
			   trabaja.rut_empresa='%s'
			   and trabaja.procesado='%s'
			   ORDER BY t.apellido_paterno_trabajador, 
			   t. apellido_materno_trabajador,
			   t.nombres_trabajador
			"""%(self.rut_empresa_actual,0)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append([i[0],i[1]+" "+i[2]+" "+i[3]])

	def define_vista_Procesados(self):
		lbl = unicode('R.U.T. Trabajador')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewTrabajadoresProcesados.append_column(column)
		lbl = unicode('Trabajador')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewTrabajadoresProcesados.append_column(column)

	def crea_modelo_Procesados(self):
		self.modelo_procesados = gtk.ListStore(str, str)
		self.treeviewTrabajadoresProcesados.set_model(self.modelo_procesados)

	def lista_datos_Procesados(self):
		self.modelo_procesados.clear()
		devolucion=[]
		devolucion.append("trabajador.rut_trabajador")
		devolucion.append("trabajador.nombres_trabajador")
		devolucion.append("trabajador.apellido_paterno_trabajador")
		devolucion.append("trabajador.apellido_materno_trabajador")
		
		
		sql="""SELECT t.rut_trabajador, t.nombres_trabajador,
			   t.apellido_paterno_trabajador, t. apellido_materno_trabajador
			   FROM trabajador t, trabaja
			   WHERE trabaja.rut_trabajador=t.rut_trabajador and
			   trabaja.rut_empresa='%s'
			   and trabaja.procesado='%s'
			   ORDER BY t.apellido_paterno_trabajador,
			   t. apellido_materno_trabajador,
			   t.nombres_trabajador
			"""%(self.rut_empresa_actual,1)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo_procesados.append([i[0],i[1]+" "+i[2]+" "+i[3]])


	def on_treeviewTrabajadoresNoProcesados_row_activated(self, tree, row, column):
		self.movimientopersonal = MovimientoPersonal(self.cursor)
		self.movimientopersonal.padre = self.padre
		self.movimientopersonal.dialog1.show_all()
		self.padre.vbox1.set_sensitive(False)
		self.padre.listatrabajadores.toolbuttonAdelante.set_sensitive(True)
		self.movimientopersonal.comboboxentryMovimientoPersonal.set_sensitive(True)
		self.movimientopersonal.entryNombreTrabajador.set_text(self.modelo[row][1])
		self.padre.t_pl_antecedentesliquidacion.rut_trabajador=self.modelo[row][0]
		self.rut_trabajador=self.modelo[row][0]
		self.row=row
		return
	
	def on_treeviewTrabajadoresProcesados_row_activated(self, tree, row, column):
		self.movimientopersonal = MovimientoPersonal(self.cursor)
		self.movimientopersonal.padre = self.padre
		self.movimientopersonal.dialog1.show_all()
		self.padre.vbox1.set_sensitive(False)
		self.padre.listatrabajadores.toolbuttonAdelante.set_sensitive(True)
		self.movimientopersonal.comboboxentryMovimientoPersonal.set_sensitive(True)
		self.movimientopersonal.entryNombreTrabajador.set_text(self.modelo_procesados[row][1])
		self.padre.t_pl_antecedentesliquidacion.rut_trabajador=self.modelo_procesados[row][0]
		self.rut_trabajador=self.modelo_procesados[row][0]
		self.row=row
		return
	
	
	def on_toolbuttonAdelante_clicked(self, toolbuttonAdelante=None):
		self.padre.notebookMain.next_page()
