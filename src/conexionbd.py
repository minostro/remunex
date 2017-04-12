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
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
from calendario import *
from dialogo_error import DialogoError
from types import StringType
from pyPgSQL.PgSQL import connect
import sys 


class Conectar_bd(GladeConnect):
	
	def __init__(self):
		GladeConnect.__init__(self, "glade/conexion_bd.glade")
		self.padre=None
		self.cursor=None
	
	
	def conectarbd(self):
		conexion="""%s:5432:%s:%s:%s"""%(
		self.entryServidor.get_text(),
		self.entryBasedeDatos.get_text(),
		self.entryUsuario.get_text(),
		self.entryContrasena.get_text()
		)
		return (connect(conexion))
		
	def on_cancelbutton1_clicked(self, cancelbutton=None):
		self.padre.conectarbd.dialog1.destroy()
		gtk.main_quit()
		return
	
	def on_okbutton1_clicked(self, okbutton=None):
		if (self.entryServidor.get_text()=="" or self.entryBasedeDatos.get_text()==""
		or self.entryUsuario.get_text()=="" or self.entryContrasena.get_text()==""):
			return
		try:
			self.padre.cnx=self.conectarbd()
			self.padre.cursor=self.padre.cnx.cursor()
			self.padre.conectarbd.dialog1.destroy()
			self.padre.windowMain.set_sensitive(True)				
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string,1)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.conectarbd.dialog1.set_sensitive(False)
			
	def on_dialog1_delete_event(self, Widget=None, Event=None):
		gtk.main_quit()
		
	def on_entryServidor_activate(self, widget=None, boton=None):
		self.on_okbutton1_clicked()
		return
