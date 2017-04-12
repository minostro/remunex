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
import pygtk
pygtk.require('2.0')
import gtk
import sys
from dialogo_error import DialogoError
from types import StringType


class Descuento(GladeConnect):
	
	def __init__(self,cursor,padre):
		GladeConnect.__init__(self, "glade/descuentos.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre =padre
		self.pk_descuento = None
		self.entryNombre.set_sensitive(False)
		self.textviewDescripcion.set_sensitive(False)
		self.entryValor.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.crea_modelo()
		self.define_vista()
		self.lista_datos()


	def define_vista(self):
		lbl = unicode('Nombre Descuento')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewDescuentos.append_column(column)
		lbl = unicode('Descripcion')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewDescuentos.append_column(column)
		lbl = unicode('Valor')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewDescuentos.append_column(column)
		

	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str, str)
		self.treeviewDescuentos.set_model(self.modelo)
		
	
	def lista_datos(self):
		self.modelo.clear()
		
		sql="""SELECT nombre_descuento, descripcion_descuento, valor_descuento 
			   FROM descuento
			   WHERE rut_empresa='%s'
			   ORDER BY nombre_descuento
			"""%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()

		for i in r:
			self.modelo.append(i)
		return

	
	def on_treeviewDescuentos_row_activated(self, tree, row, column):
		sql	=   """
				SELECT codigo_descuento
				FROM descuento 
				WHERE nombre_descuento='%s' and
				descripcion_descuento='%s' and
				valor_descuento='%s' and
				rut_empresa='%s'
				"""%(
				self.modelo[row][0],
				self.modelo[row][1],
				self.modelo[row][2],
				self.padre.rut_empresa_actual
				)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		self.pk_descuento=r[0][0]
		self.entryNombre.set_text(self.modelo[row][0])
		textbuffer=self.textviewDescripcion.get_buffer()
		textbuffer.set_text(self.modelo[row][1])
		self.entryValor.set_text(self.modelo[row][2])
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(True)
		#poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.textviewDescripcion.set_sensitive(True)
		self.entryValor.set_sensitive(True)
		#foco en codigo
		self.entryNombre.grab_focus() 

	def on_toolbuttonNuevo_clicked(self, toolbuttonNuevo=None):
		#Poniendo editable a las cajas 
		self.entryNombre.set_sensitive(True)
		self.textviewDescripcion.set_sensitive(True)
		self.entryValor.set_sensitive(True)
		#BORRA EL CONTENIDO DE LAS CAJAS DE TEXTO
		self.entryNombre.set_text("")
		textbuffer=self.textviewDescripcion.get_buffer()
		textbuffer.set_text("")
		self.entryValor.set_text("")
		#Deja sensible a anadir
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#foco en nombre
		self.entryNombre.grab_focus()
		
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadirAfp=None):
		if self.entryNombre.get_text()=="":
			return
		textbuffer=self.textviewDescripcion.get_buffer()
		startiter, enditer = textbuffer.get_bounds()
		try:
			sql	="""
				 INSERT INTO descuento
				 (rut_empresa,nombre_descuento,
				 descripcion_descuento, valor_descuento
				 )
				 VALUES ('%s','%s','%s','%s')
				 """%(
				 self.padre.rut_empresa_actual,
				 self.entryNombre.get_text().upper(),
				 textbuffer.get_text(startiter, enditer).upper(),
				 self.entryValor.get_text(),
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
		
		
	
	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizarAfp=None):
		if self.entryNombre.get_text()=="":
			return
		try:
			textbuffer=self.textviewDescripcion.get_buffer()
			startiter, enditer = textbuffer.get_bounds()
			sql	="""
				 UPDATE descuento
				 SET 
				 nombre_descuento='%s',descripcion_descuento='%s',
				 valor_descuento='%s'
				 WHERE codigo_descuento='%s'
				 """%(
				 self.entryNombre.get_text().upper(),
				 textbuffer.get_text(startiter, enditer).upper(),
				 self.entryValor.get_text(),
				 self.pk_descuento
				 )
			print sql
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
		
		
	def on_toolbuttonQuitar_clicked(self, toolbuttonQuitarAfp=None):
		try:
			sql	="""
				 DELETE FROM descuento
				 WHERE codigo_descuento='%s'
				 """%(self.pk_descuento)
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
