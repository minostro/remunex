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
import gobject
from pyPgSQL.PgSQL import connect
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
import sys

class ConexionEmpresa(GladeConnect):
	"agregar comentario"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/conexionempresa.glade")
		self.ventana_activa = None
		self.padre = None
		self.windowsEscogerEmpresa.show()
		self.comboboxentryEscogerEmpresa.child.set_sensitive(False)
		self.cursor=cursor
		#metodo para los comboboxentry empleador
		self.crear_combos_modelo()
		self.llenar_combos()

	def llenar_combos(self):
		self.modelo_empleador.clear()
		sql="""SELECT rut_empresa, razon_social
			   FROM empleador
			   ORDER BY rut_empresa
			"""
		self.cursor.execute(sql)
		self.r=self.cursor.fetchall()
		for i in self.r:
			self.modelo_empleador.append([i[1]])
						
	def crear_combos_modelo(self):
		self.modelo_empleador= gtk.ListStore(str) 
		self.comboboxentryEscogerEmpresa.set_model(self.modelo_empleador)
		cell=gtk.CellRendererText()
		self.comboboxentryEscogerEmpresa.pack_start(cell,True)
		self.comboboxentryEscogerEmpresa.add_attribute(cell,'text',0)
		return

	def on_comboboxentryEscogerEmpresa_changed(self,combo=None):
		model_aux = self.comboboxentryEscogerEmpresa.get_model()
		active = self.comboboxentryEscogerEmpresa.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.padre.rut_empresa_actual=self.r[active][0]
		self.comboboxentryEscogerEmpresa.child.set_text(elemento)
		return

	def on_okbutton1_clicked(self, boton=None):
		if self.comboboxentryEscogerEmpresa.child.get_text()=="":
			return
		if self.padre.pi.has_key("presentacion"):
			self.padre.notebookMain.remove_page(0)
			self.padre.notebookMain.set_show_tabs(True)
			self.padre.pi={}
			
		if len(self.padre.wins):
				aux=self.padre.wins
				for i in aux:
					self.padre.notebookMain.remove_page(0)
				self.padre.wins={}
		self.windowsEscogerEmpresa.hide()
		self.padre.conectar.set_sensitive(False)
		self.padre.desconectar.set_sensitive(True)
		self.padre.trabaja2.set_sensitive(True)
		self.padre.parametros_generales.set_sensitive(True)
		self.padre.parametros_especificos.set_sensitive(True)
		self.padre.especificos.set_sensitive(True)
		sql	="""SELECT fecha_proceso
		FROM proceso_remuneracion
		WHERE estado_proceso='ABIERTO' and
		rut_empresa='%s'
		"""%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			self.padre.cerrar_proceso1.set_sensitive(False)
			self.padre.liquidacion_de_sueldo1.set_sensitive(False)
			self.padre.libro_remuneraciones.set_sensitive(False)
		else:
			self.padre.nuevo_proceso1.set_sensitive(False)
		
		sql	="""SELECT fecha_proceso
		FROM proceso_remuneracion
		WHERE estado_proceso='CERRADO' and
		rut_empresa='%s'
		"""%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			self.padre.imprimir2.set_sensitive(False)
		else:
			self.padre.imprimir2.set_sensitive(True)
		
		return

	def on_cancelbutton1_clicked(self,boton=None):
		self.windowsEscogerEmpresa.hide()
