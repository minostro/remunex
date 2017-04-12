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
import gtk
from gtk import TRUE, FALSE

class ProcesarLiquidacion(GladeConnect):
	"agregar comentario"
	
	def __init__(self):
		GladeConnect.__init__(self, "glade/t_pl.glade")
		self.ventana_activa = None
		self.padre = None
		self.radiobuttonUnoaUno.set_active(True)
		self.dialogProcesar.show()

	def on_okbutton1_clicked(self, boton=None):
		if not self.padre.wins.has_key("Seleccionar Trabajador"):
			if len(self.padre.wins):
				aux=self.padre.wins
				for i in aux:
					self.padre.notebookMain.remove_page(0)
				self.padre.wins={}	
		
		if self.radiobuttonUnoaUno.get_active():
			self.padre.construir_ventanas_liquidacion_sueldo_uno_a_uno()
		
		if self.radiobuttonTodos.get_active():
			print "Todos"
			
		self.padre.liquidacion_de_sueldo1.set_sensitive(False)
		self.padre.gestion_de_trabajador1.set_sensitive(True)
		self.dialogProcesar.hide()
		
		
		return

	def on_cancelbutton1_clicked(self,boton=None):
		self.dialogProcesar.hide()
