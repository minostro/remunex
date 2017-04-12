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
import re
import gobject
import pygtk
import sys
pygtk.require('2.0')
import gtk
from dialogo_error import DialogoError
from types import StringType


class TramosCargasFamiliares(GladeConnect):
	"Actualiza las Cargas Familiares"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/pe_tramoscargasfamiliares.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.pk_tramo_carga_familiar=None
		self.regexp=re.compile("[0-9]+")
		self.id_contexto=self.statusbar1.get_context_id("Barra de estado")
		self.define_vista()

	def define_vista(self):
		sql="""SELECT *
			   FROM tramo_carga_familiar
			"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			id_mensaje=self.statusbar1.push(self.id_contexto,"Debe establecer Tramos cargas familiares")
			self.toolbuttonAnadir.set_sensitive(True)
			self.toolbuttonModificar.set_sensitive(False)
			self.toolbuttonActualizar.set_sensitive(False)	
		else:
			id_mensaje=self.statusbar1.push(self.id_contexto,"Puede modificar Tramos cargas familiares")
			self.toolbuttonAnadir.set_sensitive(False)
			self.toolbuttonModificar.set_sensitive(True)
			self.toolbuttonActualizar.set_sensitive(False)	
			self.llenar_cajas(r)
		
		
	def llenar_cajas(self,r):
		self.pk_tramo_carga_familiar=r[0][0]
		cadena=str(r[0][1])
		numeros=self.regexp.findall(cadena)
		resultado=[str(i) for i in numeros]
		
		self.entryDesde1.set_text(resultado[0])
		self.entryHasta1.set_text(resultado[1])
		self.entryValor1.set_text(resultado[2])
		
		self.entryDesde2.set_text(resultado[3])
		self.entryHasta2.set_text(resultado[4])
		self.entryValor2.set_text(resultado[5])
		
		self.entryDesde3.set_text(resultado[6])
		self.entryHasta3.set_text(resultado[7])
		self.entryValor3.set_text(resultado[8])
		
		self.entryDesde4.set_text(resultado[9])
		self.entryHasta4.set_text(resultado[10])
		self.entryValor4.set_text(resultado[11])
		
		self.entryDesde1.set_sensitive(False)
		self.entryHasta1.set_sensitive(False)
		self.entryValor1.set_sensitive(False)
		
		self.entryDesde2.set_sensitive(False)
		self.entryHasta2.set_sensitive(False)
		self.entryValor2.set_sensitive(False)
		
		self.entryDesde3.set_sensitive(False)
		self.entryHasta3.set_sensitive(False)
		self.entryValor3.set_sensitive(False)
		
		self.entryDesde4.set_sensitive(False)
		self.entryHasta4.set_sensitive(False)
		self.entryValor4.set_sensitive(False)
		
	def on_toolbuttonModificar_clicked(self, toolbuttonModificar=None):
		self.toolbuttonModificar.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.statusbar1.pop(self.id_contexto)
		id_mensaje=self.statusbar1.push(self.id_contexto,"Modificando Tramos cargas familiares")
		#poniendo editable a las cajas 
		self.entryDesde1.set_sensitive(True)
		self.entryHasta1.set_sensitive(True)
		self.entryValor1.set_sensitive(True)
		
		self.entryDesde2.set_sensitive(True)
		self.entryHasta2.set_sensitive(True)
		self.entryValor2.set_sensitive(True)
		
		self.entryDesde3.set_sensitive(True)
		self.entryHasta3.set_sensitive(True)
		self.entryValor3.set_sensitive(True)
		
		self.entryDesde4.set_sensitive(True)
		self.entryHasta4.set_sensitive(True)
		self.entryValor4.set_sensitive(True)		
	

	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadir=None):
		datos=[]
		datos.append(self.entryDesde1.get_text())
		datos.append(self.entryHasta1.get_text())
		datos.append(self.entryValor1.get_text())
		
		datos.append(self.entryDesde2.get_text())
		datos.append(self.entryHasta2.get_text())
		datos.append(self.entryValor2.get_text())
		
		datos.append(self.entryDesde3.get_text())
		datos.append(self.entryHasta3.get_text())
		datos.append(self.entryValor3.get_text())
		
		datos.append(self.entryDesde4.get_text())
		datos.append(self.entryHasta4.get_text())
		datos.append(self.entryValor4.get_text())
				
		if len(datos)==0:
			return
		try:
			sql="""INSERT INTO tramo_carga_familiar 
				(tramo_carga_familiar) 
				VALUES
				('{{%s,%s,%s},{%s,%s,%s},{%s,%s,%s},{%s,%s,%s}}')
				"""%(
				datos[0],datos[1],datos[2],
				datos[3],datos[4],datos[5],
				datos[6],datos[7],datos[8],
				datos[9],datos[10],datos[11],
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


	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizarAfp=None):
		datos=[]
		datos.append(self.entryDesde1.get_text())
		datos.append(self.entryHasta1.get_text())
		datos.append(self.entryValor1.get_text())
		
		datos.append(self.entryDesde2.get_text())
		datos.append(self.entryHasta2.get_text())
		datos.append(self.entryValor2.get_text())
		
		datos.append(self.entryDesde3.get_text())
		datos.append(self.entryHasta3.get_text())
		datos.append(self.entryValor3.get_text())
		
		datos.append(self.entryDesde4.get_text())
		datos.append(self.entryHasta4.get_text())
		datos.append(self.entryValor4.get_text())

		try:
			sql="""UPDATE tramo_carga_familiar 
				SET
				tramo_carga_familiar='{{%s,%s,%s},{%s,%s,%s},{%s,%s,%s},{%s,%s,%s}}'
				WHERE codigo_tramo_carga_familiar='%s'
				"""%(
				datos[0],datos[1],datos[2],
				datos[3],datos[4],datos[5],
				datos[6],datos[7],datos[8],
				datos[9],datos[10],datos[11],
				self.pk_tramo_carga_familiar
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
