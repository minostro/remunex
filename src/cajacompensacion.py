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

class CajaCompensacion(GladeConnect):
	"Crea, Modifica, Actualiza las Cajas de compensaciones"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/cajacompensacion.glade")
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
		self.treeviewCajaCompensacion.append_column(column)
		lbl = unicode('Razon Social')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewCajaCompensacion.append_column(column)
		
	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str)
		self.treeviewCajaCompensacion.set_model(self.modelo)
		
	def lista_datos(self):
		self.modelo.clear()
		
		sql	="""
			 SELECT nombre_caja_compensacion, razon_social_caja_compensacion
			 FROM caja_compensacion
			 ORDER BY nombre_caja_compensacion
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		for i in r:
			self.modelo.append(i)
		return

	def on_treeviewCajaCompensacion_row_activated(self, tree, row, column):
		sql	="""
			 SELECT *
			 FROM caja_compensacion WHERE nombre_caja_compensacion='%s'
			 ORDER BY nombre_caja_compensacion
			 """%(self.modelo[row][0])
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		self.pk_caja_compensacion=r[0][0]
		self.entryNombre.set_text(r[0][0])
		self.entryRazonSocial.set_text(r[0][1])
		#poniendo botones como corresponden
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(True)
		#poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)		
		
	def on_toolbuttonNuevoCajaCompensacion_clicked(self, toolbuttonNuevoCajaCompensacion=None):
		#poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		#borra el contenido de las cajas de texto
		self.entryNombre.set_text("")
		self.entryRazonSocial.set_text("")
		#poniendo disponible el boton de anadir
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#foco en codigo
		self.entryNombre.grab_focus()
	
	def on_toolbuttonAnadirCajaCompensacion_clicked(self, toolbuttonAnadirCajaCompensacion=None):
		if self.entryNombre.get_text() == "":
			return
		
		try:
			sql ="""
				 INSERT INTO caja_compensacion
				 VALUES ('%s','%s')
				 """%(
				 self.entryNombre.get_text().upper(),
				 self.entryRazonSocial.get_text().upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()
			
			self.lista_datos()
			self.on_toolbuttonNuevoCajaCompensacion_clicked()
			self.padre.empleador.llenar_combos_caja()
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
	

	def on_toolbuttonActualizarCajaCompensacion_clicked(self, toolbuttonActualizarCajaCompensacion=None):
		if self.entryNombre.get_text()=="":
			return
		
		try:
			sql	="""
				 UPDATE caja_compensacion
				 SET 
				 nombre_caja_compensacion='%s',razon_social_caja_compensacion='%s'
				 WHERE nombre_caja_compensacion='%s'
				 """%(
				 self.entryNombre.get_text().upper(),
				 self.entryRazonSocial.get_text().upper(),
				 self.pk_caja_compensacion.upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()
				
			self.lista_datos()
			self.on_toolbuttonNuevoCajaCompensacion_clicked()
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

	
	def on_toolbuttonQuitarCajaCompensacion_clicked(self, toolbuttonQuitarCajaCompensacion=None ):
		try:
			sql	="""
				 DELETE FROM caja_compensacion
				 WHERE nombre_caja_compensacion='%s'
				 """%(self.pk_caja_compensacion.upper())
			self.cursor.execute(sql)
			self.padre.cnx.commit()
		
			self.lista_datos()
			self.on_toolbuttonNuevoCajaCompensacion_clicked()
		
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
