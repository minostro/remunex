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


class BonoViajes(GladeConnect):
	
	def __init__(self,cursor,rut_empresa_actual):
		GladeConnect.__init__(self, "glade/bono_viajes.glade")
		self.cursor=cursor
		self.padre = None
		self.pk_direccion = None
		self.rut_empresa_actual=rut_empresa_actual
		#poniendo no editable a las cajas 
		self.entryOrigen.set_sensitive(False)
		self.entryDestino.set_sensitive(False)
		self.entryOrigen2.set_sensitive(False)
		self.entryValorChofer.set_sensitive(False)
		self.entryValorAuxiliar.set_sensitive(False)
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(True)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#pone el foco en codigo
		self.entryOrigen.grab_focus()
		#metodo para treeview
		self.define_vista()
		self.crea_modelo()
		self.lista_datos()


	def define_vista(self):
		lbl = unicode('Codigo Tramo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewBonoViajes.append_column(column)
		lbl = unicode('Tramo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewBonoViajes.append_column(column)
		lbl = unicode('Valor Asignado Chofer')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewBonoViajes.append_column(column)
		lbl = unicode('Valor Asignado Auxiliar')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewBonoViajes.append_column(column)

	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str, str,str)
		self.treeviewBonoViajes.set_model(self.modelo)
		
	
	def lista_datos(self):
		self.modelo.clear()
		
		sql="""SELECT codigo_vuelta, 
		nombre_vuelta, 
		valor_vuelta_chofer, 
		valor_vuelta_auxiliar
		FROM vuelta
		ORDER BY codigo_vuelta
		"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()

		for i in r:
			self.modelo.append(i)
		return

	def on_entryValorChofer_changed(self, objeto=None):
		if self.entryValorChofer.get_text()=="":
			self.entryValorAuxiliar.set_text("")
			return
		self.entryValorAuxiliar.set_text(str(int(self.entryValorChofer.get_text())/2))
	
	
	def on_treeviewBonoVueltas_row_activated(self, tree, row, column):
		self.pk_vuelta=self.modelo[row][0]
		r=self.modelo[row][1].split("-")
		self.entryOrigen.set_text(r[0])
		self.entryDestino.set_text(r[1])
		self.entryValorChofer.set_text(str(self.modelo[row][2]))
		self.entryValorAuxiliar.set_text(str(self.modelo[row][3]))
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(True)
		#poniendo editable a las cajas 
		self.entryOrigen.set_sensitive(True)
		self.entryDestino.set_sensitive(True)
		self.entryOrigen2.set_sensitive(True)
		self.entryValorChofer.set_sensitive(True)
		self.entryValorAuxiliar.set_sensitive(True)
		#foco en codigo
		self.entryOrigen.grab_focus() 

	def on_toolbuttonNuevo_clicked(self, toolbuttonNuevo=None):
		#Poniendo editable a las cajas 
		self.entryOrigen.set_sensitive(True)
		self.entryDestino.set_sensitive(True)
		self.entryOrigen2.set_sensitive(True)
		self.entryValorChofer.set_sensitive(True)
		self.entryValorAuxiliar.set_sensitive(True)
		#BORRA EL CONTENIDO DE LAS CAJAS DE TEXTO
		self.entryOrigen.set_text("")
		self.entryDestino.set_text("")
		self.entryOrigen2.set_text("")
		self.entryValorChofer.set_text("")
		self.entryValorAuxiliar.set_text("")
		#Deja sensible a anadir
		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#foco en origen
		self.entryOrigen.grab_focus()
		
	
	def on_entryOrigen_changed(self, entryOrigen=None):
		self.entryOrigen2.set_text(self.entryOrigen.get_text())
		return		
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadirAfp=None):
		if self.entryOrigen.get_text()=="":
			return
		cadena=self.entryOrigen.get_text().upper() +"-"+ self.entryDestino.get_text().upper() +"-"+ self.entryOrigen.get_text().upper()

		try:
			sql	="""
				 INSERT INTO vuelta 
				 (nombre_vuelta, valor_vuelta_chofer,
				 valor_vuelta_auxiliar)
				 VALUES ('%s','%s','%s')
				 """%(
				 cadena,
				 self.entryValorChofer.get_text(),
				 self.entryValorAuxiliar.get_text(),
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
		if self.entryDestino.get_text()=="":
			return
		cadena=self.entryOrigen.get_text().upper() +"-"+ self.entryDestino.get_text().upper() +"-"+ self.entryOrigen.get_text().upper()
		try:
			sql	="""
				 UPDATE vuelta
				 SET 
				 nombre_vuelta='%s',valor_vuelta_chofer='%s',
				 valor_vuelta_auxiliar='%s'
				 WHERE codigo_vuelta='%s'
				 """%(
				 cadena,
				 self.entryValorChofer.get_text(),
				 self.entryValorAuxiliar.get_text(),
				 self.pk_vuelta
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
		
		
	def on_toolbuttonQuitar_clicked(self, toolbuttonQuitarAfp=None):
		try:
			sql	="""
				 DELETE FROM vuelta
				 WHERE codigo_vuelta='%s'
				 """%(self.pk_vuelta)
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
