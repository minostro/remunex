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
import calendar


class Anticipos(GladeConnect):
	def __init__(self,cursor,padre,rut_trabajador):
		GladeConnect.__init__(self, "glade/anticipos.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = padre
		self.pk_direccion = None
		self.rut_trabajador=rut_trabajador
		self.comboboxentryAutorizado.child.set_sensitive(False)
		sql	="""SELECT fecha_proceso
				FROM proceso_remuneracion
				WHERE rut_empresa='%s' 
				AND estado_proceso='ABIERTO'  
			"""%(self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		self.r=self.cursor.fetchall()
		self.spinbuttonDia.set_range(1,calendar.monthrange(int(self.r[0][0].strftime("%Y")),int(self.r[0][0].strftime("%m")))[1])
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		#metodo para treeview
		self.define_vista()
		self.crea_modelo()
		self.lista_datos()


	def define_vista(self):
		lbl = unicode('Codigo')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewAnticipos.append_column(column)
		lbl = unicode('Fecha')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewAnticipos.append_column(column)
		lbl = unicode('Valor')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewAnticipos.append_column(column)
		lbl = unicode('Autorizado por:')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewAnticipos.append_column(column)

	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str, str,str)
		self.treeviewAnticipos.set_model(self.modelo)
		
	
	def lista_datos(self):
		self.modelo.clear()
		
		sql="""SELECT a.codigo_anticipo,
		a.fecha_anticipo,
		valor_anticipo,otorgado_por
		FROM anticipo a, trabajador t,
		empleador e			
		WHERE a.rut_trabajador=t.rut_trabajador and
		a.rut_empresa=e.rut_empresa and
		a.rut_trabajador='%s' and
		a.rut_empresa='%s' and
		a.fecha_anticipo <='%s' and
		a.fecha_anticipo >='%s'
		ORDER BY codigo_anticipo
		"""%(self.rut_trabajador,
		self.padre.rut_empresa_actual,
		"%s-%s-%s"%(self.r[0][0].strftime("%Y"), 
					self.r[0][0].strftime("%m"),
					calendar.monthrange(int(self.r[0][0].strftime("%Y")),int(self.r[0][0].strftime("%m")))[1]),
		"%s-%s-%s"%(self.r[0][0].strftime("%Y"), 
					self.r[0][0].strftime("%m"),
					1)
		)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()

		for i in range(len(r)):
			self.modelo.append([r[i][0],r[i][1].strftime("%Y-%m-%d"),r[i][2],r[i][3]])
		return

	def on_toolbuttonNuevo_clicked(self,boton=None):
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		self.toolbuttonAnadir.set_sensitive(True)
		self.spinbuttonDia.set_sensitive(True)
		self.entryValor.set_sensitive(True)
		self.spinbuttonDia.set_text("1")
		self.entryValor.set_text("")
		self.comboboxentryAutorizado.child.set_text("")
		return
	
	def on_treeviewDescuentos_row_activated(self, tree, row, column):
		self.pk_anticipo=self.modelo[row][0]
		cadena=self.modelo[row][1]
		self.spinbuttonDia.set_text(cadena[8]+cadena[9])
		self.entryValor.set_text(self.modelo[row][2])
		self.comboboxentryAutorizado.child.set_text(self.modelo[row][3])
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAnadir.set_sensitive(False)
		self.toolbuttonActualizar.set_sensitive(True)
		self.toolbuttonQuitar.set_sensitive(True)
		#poniendo editable a las cajas 
		self.spinbuttonDia.set_sensitive(True)
		self.entryValor.set_sensitive(True)
		#foco en codigo
		self.spinbuttonDia.grab_focus() 
		
	
	def on_toolbuttonAnadir_clicked(self, toolbuttonAnadirAfp=None):
		if self.entryValor.get_text()=="":
			return
		if self.comboboxentryAutorizado.child.get_text()=="":
			return
		try:
			cadena="%s-%s-%s"%(
			self.r[0][0].strftime("%Y"),
			self.r[0][0].strftime("%m"),
			self.spinbuttonDia.get_text()
			)
			sql	="""
				 INSERT INTO anticipo
				 (rut_empresa, rut_trabajador,
				 fecha_anticipo,valor_anticipo,otorgado_por)
				 VALUES ('%s','%s','%s','%s','%s')
				 """%(
				 self.padre.rut_empresa_actual,
				 self.rut_trabajador,
				 cadena,
				 self.entryValor.get_text(),
				 self.comboboxentryAutorizado.child.get_text(),
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
		if self.entryValor.get_text()=="":
			return
		if self.comboboxentryAutorizado.child.get_text()=="":
			return
		try:
			cadena="%s-%s-%s"%(
			self.r[0][0].strftime("%Y"),
			self.r[0][0].strftime("%m"),
			self.spinbuttonDia.get_text()
			)
			sql	="""
				 UPDATE anticipo
				 SET 
				 fecha_anticipo='%s',valor_anticipo='%s',
				 otorgado_por='%s'
				 WHERE codigo_anticipo='%s'
				 """%(
				 cadena,
				 self.entryValor.get_text(),
				 self.comboboxentryAutorizado.child.get_text(),
				 self.pk_anticipo
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
				 DELETE FROM anticipos
				 WHERE codigo_anticipo='%s'
				 """%(self.pk_anticipo)
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
	
	def on_toolbuttonCerrar_clicked(self, toolbutton=None):
		self.padre.vbox1.set_sensitive(True)
		self.llenar_valor_anticipos()
		self.window1.hide()

	def on_window1_delete_event(self, Widget=None, Event=None):
		self.padre.vbox1.set_sensitive(True)
		self.llenar_valor_anticipos()
		self.window1.hide()
		
	def llenar_valor_anticipos(self):
		iterador= self.modelo.get_iter_first()
		suma=0
		while not iterador==None:
			suma=suma+int(self.modelo.get_value(iterador,2))
			iterador= self.modelo.iter_next(iterador)
		self.padre.t_pl_antecedentesliquidacion.entryAnticipos.set_text(str(suma))
		return
