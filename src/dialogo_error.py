#!/usr/bin/env python

############################################################################
#    Copyright (C) 2005 by												   #
#                                                                          #
#        Milton Inostroz Aguilera        						           #
#           minostro@gmail.com              					           #
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

import gobject
from GladeConnect import GladeConnect
from pyPgSQL.PgSQL import connect
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
import sys
from types import StringType

class DialogoError(GladeConnect):

	def __init__(self, texto, marca=None):
		GladeConnect.__init__(self, "glade/dialogo_error.glade")
		self.padre=None
		self.marca=marca
		label = gtk.Label(texto)
		self.vbox1.pack_start(label,False, True)
		
	def on_okbutton1_clicked(self, okbutton=None):
		self.dialog1.destroy()
		if self.marca==None:
			self.padre.vbox1.set_sensitive(True)
		elif self.marca==1:
			self.padre.conectarbd.dialog1.set_sensitive(True)
		
	def on_dialog1_delete_event(self, Widget=None, Event=None):
		if self.marca==None:
			self.padre.vbox1.set_sensitive(True)
		elif self.marca==1:
			self.padre.conectarbd.dialog1.set_sensitive(True)
		return False
