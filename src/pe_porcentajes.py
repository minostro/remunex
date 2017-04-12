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
#from pyPgSQL.PgSQL import connect
import sys
import gobject
import pygtk
pygtk.require('2.0')
import gtk
from dialogo_error import DialogoError
from types import StringType

class Porcentajes(GladeConnect):
	
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/pe_porcentajes.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.pk_codigo_porcentaje=None
		self.pk_fecha_proceso=None
		self.id_contexto=self.statusbar1.get_context_id("Barra de estado")
		self.define_vista()

	def define_vista(self):
		sql="""SELECT *
			   FROM porcentaje
			"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			id_mensaje=self.statusbar1.push(self.id_contexto,"Debe establecer Porcentajes")
			self.toolbuttonAnadir.set_sensitive(True)
			self.toolbuttonModificar.set_sensitive(False)
			self.toolbuttonActualizar.set_sensitive(False)	
		else:
			id_mensaje=self.statusbar1.push(self.id_contexto,"Puede modificar Porcentajes")
			self.toolbuttonAnadir.set_sensitive(False)
			self.toolbuttonModificar.set_sensitive(True)
			self.toolbuttonActualizar.set_sensitive(False)	
			self.llenar_cajas(r)
		
	def llenar_cajas(self,r):
		self.pk_codigo_porcentaje=r[0][0]
		self.entryPorcentajeSalud.set_text(str(r[0][1]))
		self.entryPorcentajeCaja.set_text(str(r[0][2]))
		self.entryPorcentajeAdicionalLey16744.set_text(str(r[0][3]))
		self.entryPorcentajeAporteIndemnizacion.set_text(str(r[0][4]))
		self.entrySeguroCesantiaEmpleador.set_text(str(r[0][5]))
		self.entrySeguroCesantiaTrabajador.set_text(str(r[0][6]))
		self.entryPorcentajeAfpJubilados.set_text(str(r[0][7]))

		self.entryPorcentajeSalud.set_sensitive(False)
		self.entryPorcentajeCaja.set_sensitive(False)
		self.entryPorcentajeAdicionalLey16744.set_sensitive(False)
		self.entryPorcentajeAporteIndemnizacion.set_sensitive(False)
		self.entrySeguroCesantiaEmpleador.set_sensitive(False)
		self.entrySeguroCesantiaTrabajador.set_sensitive(False)
		self.entryPorcentajeAfpJubilados.set_sensitive(False)
		
	def on_toolbuttonModificar_clicked(self, toolbuttonModificar=None):
		self.toolbuttonModificar.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.statusbar1.pop(self.id_contexto)
		id_mensaje=self.statusbar1.push(self.id_contexto,"Modificando Porcentajes")
		self.entryPorcentajeSalud.set_sensitive(True)
		self.entryPorcentajeCaja.set_sensitive(True)
		self.entryPorcentajeAdicionalLey16744.set_sensitive(True)
		self.entryPorcentajeAporteIndemnizacion.set_sensitive(True)
		self.entrySeguroCesantiaEmpleador.set_sensitive(True)
		self.entrySeguroCesantiaTrabajador.set_sensitive(True)
		self.entryPorcentajeAfpJubilados.set_sensitive(True)
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadir=None):
		try:
			sql="""INSERT INTO porcentaje
				(porcentaje_salud,porcentaje_caja,
				porcentaje_adicional_ley_16_744,
				porcentaje_aporte_indemnizacion,
				seguro_cesantia_empleador,
				seguro_cesantia_trabajador,
				porcentaje_afp_jubilados) 
				VALUES
				('%s','%s','%s','%s','%s','%s','%s')
				"""%(
				self.entryPorcentajeSalud.get_text(),
				self.entryPorcentajeCaja.get_text(),
				self.entryPorcentajeAdicionalLey16744.get_text(),
				self.entryPorcentajeAporteIndemnizacion.get_text(),
				self.entrySeguroCesantiaEmpleador.get_text(),
				self.entrySeguroCesantiaTrabajador.get_text(),
				self.entryPorcentajeAfpJubilados.get_text()
				)
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.define_vista()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return

	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizar=None):
		try:
			sql="""UPDATE porcentaje
				SET
				porcentaje_salud='%s',porcentaje_caja='%s',
				porcentaje_adicional_ley_16_744='%s',
				porcentaje_aporte_indemnizacion='%s',
				seguro_cesantia_empleador='%s',
				seguro_cesantia_trabajador='%s',
				porcentaje_afp_jubilados='%s' 
				WHERE codigo_porcentaje='%s'
				"""%(
				self.entryPorcentajeSalud.get_text(),
				self.entryPorcentajeCaja.get_text(),
				self.entryPorcentajeAdicionalLey16744.get_text(),
				self.entryPorcentajeAporteIndemnizacion.get_text(),
				self.entrySeguroCesantiaEmpleador.get_text(),
				self.entrySeguroCesantiaTrabajador.get_text(),
				self.entryPorcentajeAfpJubilados.get_text(),
				self.pk_codigo_porcentaje
				)
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.define_vista()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
