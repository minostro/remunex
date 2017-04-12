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
import time
import calendar

class NuevoProceso(GladeConnect):
	def __init__(self, cursor,tipo,padre):
		GladeConnect.__init__(self, "glade/nuevo_proceso.glade")
		self.padre=padre
		self.cursor=cursor
		self.tipo=tipo
		self.comboboxentryMes.child.set_sensitive(False)
		self.comboboxentryAnio.child.set_sensitive(False)
		if tipo==0:
			self.hboxFechaInicial.show_all()
		else:
			self.hboxNuevoProceso.show_all()	
			self.comboboxentryMes.set_sensitive(False)
			self.comboboxentryAnio.set_sensitive(False)
			sql	="""SELECT fecha_proceso
				 FROM proceso_remuneracion
				 WHERE estado_proceso='CERRADO' and
				 rut_empresa='%s'
				 ORDER BY codigo_proceso
				 """%(self.padre.rut_empresa_actual)
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			mytime = time.mktime((int(r[len(r)-1][0].strftime("%Y")),int(r[len(r)-1][0].strftime("%m"))+1,1, 0, 0, 0, 0, 0, -1))
			self.comboboxentryMes.child.set_text(time.strftime('%m',time.localtime(mytime))+"-"+time.strftime('%B',time.localtime(mytime)).upper())
			self.comboboxentryAnio.child.set_text(time.strftime('%Y',time.localtime(mytime)))
		
	def on_cancelbutton1_clicked(self, cancel=None):
		self.padre.nuevo_proceso.dialog1.destroy()
		return
	
	def on_okbutton1_clicked(self,ok=None):
		if not (self.comboboxentryMes.child.get_text()=="" or self.comboboxentryAnio.child.get_text()==""):
			mes=self.comboboxentryMes.child.get_text().split("-")[0]
			dia=calendar.monthrange(int(self.comboboxentryAnio.child.get_text()),int(mes))[1]
			try:
				sql	="""INSERT INTO proceso_remuneracion
					 (rut_empresa,fecha_proceso,
					 estado_proceso)
					 VALUES ('%s','%s','%s')
					 """%(
					 self.padre.rut_empresa_actual,
					 '%s-%s-%s'%(self.comboboxentryAnio.child.get_text(),mes,dia),
					 'ABIERTO'
					 )
				self.cursor.execute(sql)
				self.padre.cnx.commit()
				self.padre.nuevo_proceso.dialog1.destroy()
				self.padre.nuevo_proceso1.set_sensitive(False)
				self.padre.cerrar_proceso1.set_sensitive(True)
				self.padre.liquidacion_de_sueldo1.set_sensitive(True)
				self.padre.libro_remuneraciones.set_sensitive(True)
				
			except:
				string = StringType(sys.exc_info()[1])
				string = unicode(string,"iso8859-15")
				string = string.encode("utf-8")			
				dialogo_error=DialogoError(string)
				dialogo_error.dialog1.show_all()
				dialogo_error.padre=self.padre
				self.padre.vbox1.set_sensitive(False)
				return
		else:
			return
