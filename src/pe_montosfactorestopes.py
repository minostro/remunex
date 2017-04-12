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
import sys
import pygtk
pygtk.require('2.0')
import gtk
from dialogo_error import DialogoError
from types import StringType

class MontosFactoresTopes(GladeConnect):
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/pe_montosfactorestopes.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.pk_codigo_monto_factores_topes=None
		self.id_contexto=self.statusbar1.get_context_id("Barra de estado")
		self.define_vista()

	def define_vista(self):
		sql="""SELECT *
			   FROM monto_factores_topes
			"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			id_mensaje=self.statusbar1.push(self.id_contexto,"Debe establecer Montos - Factores - Topes")
			self.toolbuttonAnadir.set_sensitive(True)
			self.toolbuttonModificar.set_sensitive(False)
			self.toolbuttonActualizar.set_sensitive(False)	
		else:
			id_mensaje=self.statusbar1.push(self.id_contexto,"Puede modificar Montos - Factores - Topes")
			self.toolbuttonAnadir.set_sensitive(False)
			self.toolbuttonModificar.set_sensitive(True)
			self.toolbuttonActualizar.set_sensitive(False)	
			self.llenar_cajas(r)
	
	def llenar_cajas(self,r):
		self.pk_codigo_monto_factores_topes=r[0][0]
		self.entryUtm.set_text(str(r[0][1]))
		self.entryUf.set_text(str(r[0][2]))
		self.entryUtm.set_sensitive(False)
		self.entryUf.set_sensitive(False)
		
	def on_toolbuttonModificar_clicked(self, toolbuttonModificar=None):
		self.toolbuttonModificar.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.statusbar1.pop(self.id_contexto)
		id_mensaje=self.statusbar1.push(self.id_contexto,"Modificando Montos - Factores - Topes")
		self.entryUtm.set_sensitive(True)
		self.entryUf.set_sensitive(True)
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadir=None):
		try:
			sql	="""INSERT INTO monto_factores_topes
				(utm,uf)
				VALUES ('%s','%s')
				"""%(
				 self.entryUtm.get_text(),
				 self.entryUf.get_text(),
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
			sql	="""
				 UPDATE monto_factores_topes
				 SET 
				 utm='%s',uf='%s'				 
				 WHERE codigo_monto_factores_topes='%s'
				 """%(
				 self.entryUtm.get_text(),
				 self.entryUf.get_text(),
				 self.pk_codigo_monto_factores_topes
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
