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

class Salud(GladeConnect):
	"Crea, Modifica, Actualiza sistema de salud FONOSA o ISAPRES"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/salud.glade")
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
		self.treeviewSalud.append_column(column)
		lbl = unicode('Razon Social')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewSalud.append_column(column)
		

	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str)
		self.treeviewSalud.set_model(self.modelo)
		
	
	def lista_datos(self):
		self.modelo.clear()
		
		sql	="""
			 SELECT nombre_salud, razon_social_salud
			 FROM salud
			 ORDER BY nombre_salud
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append(i)
		return

	
	def on_treeviewSalud_row_activated(self, tree, row, column):
		sql	="""
			 SELECT *
			 FROM salud WHERE nombre_salud='%s'
			 ORDER BY nombre_salud
			 """%(self.modelo[row][0])
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		self.pk_salud=r[0][0]		
		self.entryNombre.set_text(r[0][0])
		self.entryRazonSocial.set_text(r[0][1])
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(True)
		#poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		#foco en codigo
		self.entryNombre.grab_focus() 

	def on_toolbuttonNuevo_clicked(self, toolbuttonNuevo=None):
		#Poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		#BORRA EL CONTENIDO DE LAS CAJAS DE TEXTO
		self.entryNombre.set_text("")
		self.entryRazonSocial.set_text("")
		#Deja sensible a anadir
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#foco en codigo
		self.entryNombre.grab_focus()
		
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadir=None):
		if self.entryNombre.get_text() == "":
			self.on_toolbuttonNuevo_clicked()
			return

		try:
			sql ="""
				 INSERT INTO salud
				 VALUES ('%s','%s')
				 """%(
				 self.entryNombre.get_text().upper(),
				 self.entryRazonSocial.get_text().upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			self.lista_datos()
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
		
		return
	
	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizarIsapre=None):

		if self.entryNombre.get_text()=="":
			return
		
		try:
			sql	="""
				 UPDATE salud
				 SET 
				 nombre_salud='%s',razon_social_salud='%s'
				 WHERE nombre_salud='%s'
				 """%(
				 self.entryNombre.get_text().upper(),
				 self.entryRazonSocial.get_text().upper(),
				 self.pk_salud.upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			
			self.lista_datos()
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
		
		return
		
		
	def on_toolbuttonQuitar_clicked(self, toolbuttonQuitarIsapre=None):
		try:
			sql	="""
				 DELETE FROM salud
				 WHERE nombre_salud='%s'
				 """%(self.pk_salud.upper())
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			
			self.lista_datos()
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
		return
