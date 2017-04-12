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
from dialogo_error import DialogoError
from types import StringType

class MutualSeguridad(GladeConnect):
	"Crea, Modifica, Actualiza las Mutuales de seguridad"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/mutualseguridad.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		#poniendo no editable a las cajas 
		self.entryNombre.set_sensitive(False)
		self.entryRazonSocial.set_sensitive(False)
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(True)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#pone el foco en codigo
		self.entryNombre.grab_focus()
		#metodo para treeview
		self.define_vista()
		self.crea_modelo()

	def define_vista(self):
		lbl = unicode('Nombre')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewMutualSeguridad.append_column(column)
		
		lbl = unicode('Razon Social')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewMutualSeguridad.append_column(column)
		
	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str)
		self.treeviewMutualSeguridad.set_model(self.modelo)
		
	def lista_datos(self):
		self.modelo.clear()
		
		sql	="""
			 SELECT nombre_mutual_seguridad, razon_social_mutual_seguridad
			 FROM mutual_seguridad
			 ORDER BY nombre_mutual_seguridad
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		for i in r:
			self.modelo.append(i)
		return
	

	def on_treeviewMutualSeguridad_row_activated(self, tree, row, column):
		sql	="""
			 SELECT *
			 FROM mutual_seguridad WHERE nombre_mutual_seguridad='%s'
			 ORDER BY nombre_mutual_seguridad
			 """%(self.modelo[row][0])
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		self.pk_mutual_seguridad=r[0][0]
		self.entryNombre.set_text(r[0][0])
		self.entryRazonSocial.set_text(r[0][1])
		#poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(True)
		
		
	def on_toolbuttonNuevoMutualSeguridad_clicked(self, toolbuttonNuevoMutualSeguridad=None):
		#poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		#borra el contenido de las cajas de texto
		self.entryNombre.set_text("")
		self.entryRazonSocial.set_text("")
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#foco en codigo
		self.entryNombre.grab_focus()
	
	def on_toolbuttonAnadirMutualSeguridad_clicked(self, toolbuttonAnadirMutualSeguridad=None):
		if self.entryNombre.get_text() == "":
			return
		
		try:
			sql ="""
				 INSERT INTO mutual_seguridad
				 VALUES ('%s','%s')
				 """%(
				 self.entryNombre.get_text().upper(),
				 self.entryRazonSocial.get_text().upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			
			self.lista_datos()
			self.on_toolbuttonNuevoMutualSeguridad_clicked()
			self.padre.empleador.llenar_combos_mutual()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return


	def on_toolbuttonActualizarMutualSeguridad_clicked(self, toolbuttonActualizarMutualSeguridad=None):
		
		if self.entryNombre.get_text() == "":
			return

		try:
			sql	="""
				 UPDATE mutual_seguridad
				 SET 
				 nombre_mutual_seguridad='%s',razon_social_mutual_seguridad='%s'
				 WHERE nombre_mutual_seguridad='%s'
				 """%(
				 self.entryNombre.get_text().upper(),
				 self.entryRazonSocial.get_text().upper(),
				 self.pk_mutual_seguridad.upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()
		
			self.lista_datos()
			self.on_toolbuttonNuevoMutualSeguridad_clicked()
		
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return

		return

	
	def on_toolbuttonQuitarMutualSeguridad_clicked(self, toolbuttonQuitarMutualSeguridad=None ):
		try:
			sql	="""
				 DELETE FROM mutual_seguridad
				 WHERE nombre_mutual_seguridad='%s'
				 """%(self.pk_mutual_seguridad.upper())
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			
			self.lista_datos()
			self.on_toolbuttonNuevoMutualSeguridad_clicked()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
		return
