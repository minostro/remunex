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
from pyPgSQL.PgSQL import connect
import gobject
import sys
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk
from conexionbd import *
from dialogo_error import DialogoError
from types import StringType
import string

class Empleador(GladeConnect):
	"Crea, Modifica, Actualiza los Empleadores"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/empleador.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None 
		#poniendo no editable a las cajas 
		self.entryRutEmpresa.set_sensitive(False)
		self.entryRazonSocial.set_sensitive(False)
		self.entryTelefono.set_sensitive(False)
		self.entryCalle.set_sensitive(False)
		self.entryNumero.set_sensitive(False)
		self.radiobuttonDepartamentoNo.set_sensitive(False)
		self.radiobuttonDepartamentoSi.set_sensitive(False)
		self.entryBlock.set_sensitive(False)
		self.entryDepartamento.set_sensitive(False)		
		self.entryCiudad.set_sensitive(False)
		self.comboboxentryComuna.set_sensitive(False)
		self.comboboxentryComuna.child.set_sensitive(False)
		self.entryRegion.set_sensitive(False)
		self.entryRutRepresentante.set_sensitive(False)
		self.entryNombreyApellidoRepresentante.set_sensitive(False)
		self.entryCodigoActividad.set_sensitive(False)
		self.entryGiroComercial.set_sensitive(False)
		self.comboboxentryMutualSeguridad.set_sensitive(False)
		self.comboboxentryMutualSeguridad.child.set_sensitive(False)
		self.entryNumeroAdherente.set_sensitive(False)
		self.entryPorcentajeCotizacion.set_sensitive(False)
		self.comboboxentryCajaCompensacion.set_sensitive(False)
		self.comboboxentryCajaCompensacion.child.set_sensitive(False)
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAnadirEmpleador.set_sensitive(False)
		self.toolbuttonActualizarEmpleador.set_sensitive(False)
		self.toolbuttonQuitarEmpleador.set_sensitive(False)
		#pone el foco en codigo
		self.entryRutEmpresa.grab_focus()
		#metodo para los comboboxentry
		self.crear_combos_modelo_mutual()
		self.llenar_combos_mutual()
		self.crear_combos_modelo_caja()
		self.llenar_combos_caja()
		#metodo para treeview
		self.define_vista()
		self.crea_modelo()



	def llenar_combos_mutual(self):
		self.modelo_mutual.clear()
		sql	="""
			 SELECT nombre_mutual_seguridad
			 FROM mutual_seguridad
			 ORDER BY nombre_mutual_seguridad
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo_mutual.append(i)
		return
		

	def crear_combos_modelo_mutual(self):
		self.modelo_mutual= gtk.ListStore(str) 
		self.comboboxentryMutualSeguridad.set_model(self.modelo_mutual)
		cell=gtk.CellRendererText()
		self.comboboxentryMutualSeguridad.pack_start(cell,True)
		self.comboboxentryMutualSeguridad.add_attribute(cell,'text',0)
		return

	def llenar_combos_caja(self):
		self.modelo_caja.clear()
		sql	="""
			 SELECT nombre_caja_compensacion
			 FROM caja_compensacion
			 ORDER BY nombre_caja_compensacion
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo_caja.append(i)
		return
		

	def crear_combos_modelo_caja(self):
		self.modelo_caja= gtk.ListStore(str) 
		self.comboboxentryCajaCompensacion.set_model(self.modelo_caja)
		cell=gtk.CellRendererText()
		self.comboboxentryCajaCompensacion.pack_start(cell,True)
		self.comboboxentryCajaCompensacion.add_attribute(cell,'text',0)
		return


	def define_vista(self):
		lbl = unicode('R.U.T. Empresa')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewEmpleador.append_column(column)
		lbl = unicode('Razon Social')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewEmpleador.append_column(column)
		
	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str)
		self.treeviewEmpleador.set_model(self.modelo)
		

	def lista_datos(self):
		self.modelo.clear()
		sql	="""
			 SELECT rut_empresa,razon_social 
			 FROM empleador
			 ORDER BY rut_empresa
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append(i)
		return
	

	def on_treeviewEmpleador_row_activated(self, tree, row, column):
		#llenando caja de texto
		self.pk_empleador=self.modelo[row][0]
		self.entryRutEmpresa.set_text(self.modelo[row][0])
		self.entryRazonSocial.set_text(self.modelo[row][1])
		
		sql="""SELECT e.telefono_empresa, g.codigo_actividad,
		g.nombre_actividad, d.nombre_calle_direccion,
		d.numero_direccion, d.block_direccion,
		d.departamento_direccion, l.nombre_comuna,
		e.rut_representante_empresa, e.razon_social_representante,
		e.nombre_mutual_seguridad,
		e.mutual_numero_adherente, e.mutual_porcentaje_cotizacion,
		e.nombre_caja_compensacion,
		d.codigo_direccion, g.codigo_actividad
		FROM empleador e, direccion d, localidad l, 
		giro_comercial g	   
		WHERE e.codigo_direccion=d.codigo_direccion 
		and e.codigo_actividad=g.codigo_actividad
		and d.nombre_comuna=l.nombre_comuna 
		and e.rut_empresa='%s'
		ORDER BY e.rut_empresa
		"""%(self.pk_empleador.upper())
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		
		self.entryTelefono.set_text(r[0][0])
		self.entryCodigoActividad.set_text(str(r[0][1]))
		self.entryGiroComercial.set_text(r[0][2])
		self.entryCalle.set_text(r[0][3])
		self.entryNumero.set_text(str(r[0][4]))
		if r[0][5]==None or r[0][5]==" ":
			self.radiobuttonDepartamentoNo.set_active(True)
		else:
			self.radiobuttonDepartamentoSi.set_active(True)
			self.entryBlock.set_text(r[0][5])
			self.entryDepartamento.set_text(str(r[0][6]))	
		self.comboboxentryComuna.child.set_text(r[0][7])
		self.entryRutRepresentante.set_text(r[0][8])
		self.entryNombreyApellidoRepresentante.set_text(r[0][9])
		self.comboboxentryMutualSeguridad.child.set_text(r[0][10])
		self.entryNumeroAdherente.set_text(r[0][11])
		self.entryPorcentajeCotizacion.set_text(str(r[0][12]))
		self.comboboxentryCajaCompensacion.child.set_text(r[0][13])
		self.pk_direccion=(r[0][14])
		self.pk_giro_comercial=(r[0][15])

		#dejando botones como corresponden
		self.toolbuttonNuevoEmpleador.set_sensitive(True)
		self.toolbuttonAnadirEmpleador.set_sensitive(False)
		self.toolbuttonActualizarEmpleador.set_sensitive(True)
		self.toolbuttonQuitarEmpleador.set_sensitive(True)
		#poniendo editable a las cajas 
		self.entryRutEmpresa.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		self.entryTelefono.set_sensitive(True)
		self.entryCalle.set_sensitive(True)
		self.entryNumero.set_sensitive(True)
		self.radiobuttonDepartamentoNo.set_sensitive(True)
		self.radiobuttonDepartamentoSi.set_sensitive(True)
		self.comboboxentryComuna.set_sensitive(True)
		self.entryRutRepresentante.set_sensitive(True)
		self.entryNombreyApellidoRepresentante.set_sensitive(True)
		self.entryCodigoActividad.set_sensitive(True)
		self.entryGiroComercial.set_sensitive(True)
		self.comboboxentryMutualSeguridad.set_sensitive(True)
		self.entryNumeroAdherente.set_sensitive(True)
		self.entryPorcentajeCotizacion.set_sensitive(True)
		self.comboboxentryCajaCompensacion.set_sensitive(True)
		self.comboboxentryMutualSeguridad.set_sensitive(True)
		self.comboboxentryCajaCompensacion.set_sensitive(True)
		
	def on_toolbuttonNuevoEmpleador_clicked(self, toolbuttonNuevoEmpleador=None):
		self.notebook1.set_current_page(0)
		#poniendo editable a las cajas 
		self.entryRutEmpresa.set_sensitive(True)
		self.entryRazonSocial.set_sensitive(True)
		self.entryTelefono.set_sensitive(True)
		self.entryCalle.set_sensitive(True)
		self.entryNumero.set_sensitive(True)
		self.radiobuttonDepartamentoNo.set_sensitive(True)
		self.radiobuttonDepartamentoSi.set_sensitive(True)
		self.radiobuttonDepartamentoNo.set_active(True)
		self.comboboxentryComuna.set_sensitive(True)
		self.entryRutRepresentante.set_sensitive(True)
		self.entryNombreyApellidoRepresentante.set_sensitive(True)
		self.entryCodigoActividad.set_sensitive(True)
		self.entryGiroComercial.set_sensitive(True)
		self.comboboxentryMutualSeguridad.set_sensitive(True)
		self.entryNumeroAdherente.set_sensitive(True)
		self.entryPorcentajeCotizacion.set_sensitive(True)
		self.comboboxentryCajaCompensacion.set_sensitive(True)
		self.comboboxentryMutualSeguridad.set_sensitive(True)
		self.comboboxentryCajaCompensacion.set_sensitive(True)
		#borra el contenido de las cajas
		self.entryRutEmpresa.set_text("")
		self.entryRazonSocial.set_text("")
		self.entryTelefono.set_text("")
		self.entryCalle.set_text("")
		self.entryNumero.set_text("")		
		self.entryBlock.set_text("")
		self.entryDepartamento.set_text("")	
		self.comboboxentryComuna.child.set_text("")
		self.entryRutRepresentante.set_text("")
		self.entryNombreyApellidoRepresentante.set_text("")
		self.entryCodigoActividad.set_text("")
		self.entryGiroComercial.set_text("")
		self.comboboxentryMutualSeguridad.child.set_text("")
		self.entryNumeroAdherente.set_text("")
		self.entryPorcentajeCotizacion.set_text("")
		self.comboboxentryCajaCompensacion.child.set_text("")
		self.comboboxentryMutualSeguridad.child.set_text("")
		self.comboboxentryCajaCompensacion.child.set_text("")
		#foco en en rut de empleador
		self.entryRutEmpresa.grab_focus()
		#botones
		self.toolbuttonNuevoEmpleador.set_sensitive(False)
		self.toolbuttonAnadirEmpleador.set_sensitive(True)
		self.toolbuttonActualizarEmpleador.set_sensitive(False)
		self.toolbuttonQuitarEmpleador.set_sensitive(False)

	
	def on_toolbuttonAnadirEmpleador_clicked(self, toolbuttonAnadirEmpleador=None):
		#obteniendo	datos del empleador
		empleador=[]
		
		if self.entryRutEmpresa.get_text() == "":
			self.on_toolbuttonNuevoEmpleador_clicked()
			return
		
		
		sql	="""
			 SELECT * 
			 FROM localidad WHERE nombre_comuna='%s'
			 """%(self.comboboxentryComuna.child.get_text().upper())
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		try:
			if len(r)==0:		
				sql ="""
					 INSERT INTO localidad
					 VALUES ('%s','%s','%s')
					 """%(
					 self.comboboxentryComuna.child.get_text().upper(),
					 self.entryCiudad.get_text().upper(),
					 self.entryRegion.get_text().upper()
					 )
				self.cursor.execute(sql)
				if self.radiobuttonDepartamentoSi.get_active():
					sql ="""
						 INSERT INTO direccion
						 (nombre_comuna,nombre_calle_direccion,
						  numero_direccion,block_direccion,
						  departamento_direccion
						 )
						 VALUES ('%s','%s','%s','%s','%s')
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 self.entryBlock.get_text().upper(),
						 self.entryDepartamento.get_text()
						 )
					self.cursor.execute(sql)
				else:
					sql ="""
						 INSERT INTO direccion
						 (nombre_comuna,nombre_calle_direccion,
						  numero_direccion
						 )
						 VALUES ('%s','%s',%s)
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 )
					self.cursor.execute(sql)
			else:
				if self.radiobuttonDepartamentoSi.get_active():
					sql ="""
						 INSERT INTO direccion
						 (nombre_comuna,nombre_calle_direccion,
						  numero_direccion,block_direccion,
						  departamento_direccion
						 )
						 VALUES ('%s','%s','%s','%s','%s')
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 self.entryBlock.get_text().upper(),
						 self.entryDepartamento.get_text()
						 )
					self.cursor.execute(sql)
				else:
					sql ="""
						 INSERT INTO direccion
						 (nombre_comuna,nombre_calle_direccion,
						  numero_direccion
						 )
						 VALUES ('%s','%s',%s)
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 )
					self.cursor.execute(sql)
			sql="""SELECT codigo_actividad
			FROM giro_comercial
			WHERE codigo_actividad='%s'
			"""%(self.entryCodigoActividad.get_text().upper())
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			if len(r)==0:
				sql ="""
					 INSERT INTO giro_comercial
					 VALUES ('%s','%s')
					 """%(
					 self.entryCodigoActividad.get_text().upper(),
					 self.entryGiroComercial.get_text().upper(),
					 )
				self.cursor.execute(sql)
			if self.radiobuttonDepartamentoSi.get_active():
				sql	="""
					 SELECT codigo_direccion 
					 FROM direccion WHERE
					 nombre_calle_direccion='%s' and
					 numero_direccion='%s' and
					 block_direccion='%s' and
					 departamento_direccion='%s'
					 """%(
					 self.entryCalle.get_text().upper(),
					 self.entryNumero.get_text(),
					 self.entryBlock.get_text().upper(),
					 self.entryDepartamento.get_text() 
					 )
				self.cursor.execute(sql)
				r=self.cursor.fetchall()
			else:
				sql	="""
					 SELECT codigo_direccion 
					 FROM direccion WHERE
					 nombre_calle_direccion='%s' and
					 numero_direccion='%s'
					 """%(
					 self.entryCalle.get_text().upper(),
					 self.entryNumero.get_text(),
					 )
				self.cursor.execute(sql)
				r=self.cursor.fetchall()

			empleador.append(self.entryRutEmpresa.get_text().upper())
			empleador.append(str(r[0][0]))
			empleador.append(self.comboboxentryCajaCompensacion.child.get_text().upper())			
			empleador.append(self.entryCodigoActividad.get_text().upper())
			empleador.append(self.comboboxentryMutualSeguridad.child.get_text().upper())
			empleador.append(self.entryRazonSocial.get_text().upper())
			empleador.append(self.entryTelefono.get_text())
			empleador.append(self.entryRutRepresentante.get_text().upper())
			empleador.append(self.entryNombreyApellidoRepresentante.get_text().upper())
			empleador.append(self.entryNumeroAdherente.get_text())
			empleador.append(self.entryPorcentajeCotizacion.get_text())
			
			sql ="""
				 INSERT INTO empleador
				 VALUES("""+ ",".join(["'%s'" %(n1) for n1 in empleador])+")"
			self.cursor.execute(sql)
			self.padre.cnx.commit()		
			self.lista_datos()
			self.on_toolbuttonNuevoEmpleador_clicked()
			
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			self.padre.cnx.rollback()
			return
	
		
	def on_toolbuttonActualizarEmpleador_clicked(self, toolbuttonActualizarEmpleador=None):
		if self.entryRutEmpresa.get_text() == "":
			self.on_toolbuttonNuevoEmpleador_clicked()
			return
		
		sql	="""
			 SELECT * 
			 FROM localidad WHERE nombre_comuna='%s'
			 """%(self.comboboxentryComuna.child.get_text().upper())
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		try:
			if len(r)==0:		
				sql ="""
					 INSERT INTO localidad
					 VALUES ('%s','%s','%s')
					 """%(
					 self.comboboxentryComuna.child.get_text().upper(),
					 self.entryCiudad.get_text().upper(),
					 self.entryRegion.get_text().upper()
					 )
				self.cursor.execute(sql)
				if self.radiobuttonDepartamentoSi.get_active():
					sql	="""
						 UPDATE direccion
						 SET 
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s', block_direccion='%s',
						 departamento_direccion='%s'
						 WHERE codigo_direccion='%s'
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 self.entryBlock.get_text().upper(),
						 self.entryDepartamento.get_text(),
						 self.pk_direccion
						 )					
					self.cursor.execute(sql)
				else:
					sql	="""
						 UPDATE direccion
						 SET 
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s',block_direccion=' ',
						 departamento_direccion='0' 
						 WHERE codigo_direccion='%s'
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 self.pk_direccion
						 )					
					self.cursor.execute(sql)
			else:
				if self.radiobuttonDepartamentoSi.get_active():
					sql	="""
						 UPDATE direccion
						 SET 
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s', block_direccion='%s',
						 departamento_direccion='%s'
						 WHERE codigo_direccion='%s'
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 self.entryBlock.get_text().upper(),
						 self.entryDepartamento.get_text(),
						 self.pk_direccion
						 )					
					self.cursor.execute(sql)
				else:
					sql	="""
						 UPDATE direccion
						 SET 
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s',block_direccion=' ',
						 departamento_direccion='0' 
						 WHERE codigo_direccion='%s'
						 """%(
						 self.comboboxentryComuna.child.get_text().upper(),
						 self.entryCalle.get_text().upper(),
						 self.entryNumero.get_text(),
						 self.pk_direccion
						 )					
					self.cursor.execute(sql)
						
			sql	="""
				 UPDATE giro_comercial
				 SET 
				 codigo_actividad='%s', nombre_actividad='%s'
				 WHERE codigo_actividad='%s'
				 """%(
				 self.entryCodigoActividad.get_text().upper(),
				 self.entryGiroComercial.get_text().upper(),
				 self.pk_giro_comercial
				 )
			self.cursor.execute(sql)
			sql	="""
				 UPDATE empleador
				 SET 
				 rut_empresa='%s',codigo_direccion='%s',
				 nombre_caja_compensacion='%s',
				 codigo_actividad='%s',nombre_mutual_seguridad='%s',
				 razon_social='%s',telefono_empresa='%s',
				 rut_representante_empresa='%s',razon_social_representante='%s',
				 mutual_numero_adherente='%s',mutual_porcentaje_cotizacion='%s'
				 WHERE rut_empresa='%s'
				 """%(
				 self.entryRutEmpresa.get_text().upper(),
				 self.pk_direccion,
				 self.comboboxentryCajaCompensacion.child.get_text().upper(),
				 self.entryCodigoActividad.get_text().upper(),
				 self.comboboxentryMutualSeguridad.child.get_text().upper(),
				 self.entryRazonSocial.get_text().upper(),
				 self.entryTelefono.get_text(),
				 self.entryRutRepresentante.get_text().upper(),
				 self.entryNombreyApellidoRepresentante.get_text().upper(),
				 self.entryNumeroAdherente.get_text(),
				 self.entryPorcentajeCotizacion.get_text(),
				 self.pk_empleador.upper()
				 )
			self.cursor.execute(sql)
			self.padre.cnx.commit()		
			self.lista_datos()
			self.on_toolbuttonNuevoEmpleador_clicked()
			
		except:
			print sys.exc_info()[1]
			self.padre.cnx.rollback()
			return

	def on_toolbuttonQuitarEmpleador_clicked(self, toolbuttonQuitarEmpleador=None):
		rut_empresa	=self.entryRutEmpresa.get_text()

		try:
			SentenciaSql.delete(self,"empleador","rut_empresa",rut_empresa)
			self.lista_datos()
			self.on_toolbuttonNuevoEmpleador_clicked()
			
		except:
			print sys.exc_info()[1]
			return


	def on_comboboxentryCiudad_changed(self,combo=None):
		model_aux = self.comboboxentryCiudad.get_model()
		active = self.comboboxentryCiudad.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryCiudad.child.set_text(elemento)
		devolucion=[]
		devolucion.append("nombre_comuna, nombre_region")
		diccionario={}
		diccionario["nombre_ciudad"]=(elemento)		
		r = SentenciaSql.select(self,"localidad",devolucion,"nombre_ciudad",0,diccionario)
		self.entryComuna.set_text(r[0][0])
		self.entryRegion.set_text(r[0][1])
		self.entryComuna.set_sensitive(False)
		self.entryRegion.set_sensitive(False)


	def on_comboboxentryCiudad_set_focus_child(self, combo=None, texto=None):
		self.entryComuna.set_sensitive(True)
		self.entryRegion.set_sensitive(True)
		return


	def on_comboboxentryMutualSeguridad_changed(self,combo=None):
		model_aux = self.comboboxentryMutualSeguridad.get_model()
		active = self.comboboxentryMutualSeguridad.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryMutualSeguridad.child.set_text(elemento)


	def on_comboboxentryCajaCompensacion_changed(self,combo=None):
		model_aux = self.comboboxentryCajaCompensacion.get_model()
		active = self.comboboxentryCajaCompensacion.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryCajaCompensacion.child.set_text(elemento)
	
	def on_radiobuttonDepartamentoNo_toggled(self, radiobutton=None):
		if self.radiobuttonDepartamentoNo.get_active():
			self.entryBlock.set_sensitive(False)
			self.entryDepartamento.set_sensitive(False)
			self.entryBlock.set_text("")
			self.entryDepartamento.set_text("")
		else:
			self.entryBlock.set_sensitive(True)
			self.entryDepartamento.set_sensitive(True)
			self.entryBlock.set_text("")
			self.entryDepartamento.set_text("")
	
	def formato_rut(self, rut):
		if rut == "":
			return rut
	
		rut = string.replace(rut,".","")
		rut = string.replace(rut,"-","")
		rut = "0000000000"+ rut
		l = len(rut)
		rut_aux = "-" + rut[l-1:l]
		l = l-1
		while 2 < l:
			rut_aux = "."+ rut[l-3:l] +rut_aux
			l = l-3
	
		rut_aux = rut[0:l] +rut_aux
		l = len(rut_aux)
		rut_aux = rut_aux[l-12:l]
		return rut_aux

	def es_rut(self, rut=None):
		if not rut: return 0
		es_rut = 0
		cadena = "234567234567"
		dig_rut = rut[-1]
		rut = string.replace(rut, ".", "")
		rut = rut[:rut.find("-")]
		rut = string.replace(rut, " ", '0')
		j, suma, i = 0, 0, len(rut) -1
		while i >= 0:
			try:
				suma = suma + (int(rut[i]) * int(cadena[j]))
			except:
				return 0
			i = i - 1
			j = j + 1
		divid = int(suma/11)
		mult = int(divid*11)
		dife = suma - mult
		digito = 11 - dife
		if digito == 10:
			caract = "k"
		elif digito == 11:
			caract = "0"
		else:
			caract = string.replace(str(digito), " ", "")
		if caract == dig_rut:
			es_rut = 1
		return es_rut

	def on_entryRutEmpresa_focus_out_event(self, widget=None, eventda=None):
			rut=self.formato_rut(self.entryRutEmpresa.get_text().lower())
			if self.es_rut(rut):
					self.entryRutEmpresa.set_text(rut)
			else:
					self.entryRutEmpresa.set_text("")
					
	def on_entryRutRepresentante_focus_out_event(self, widget=None, eventda=None):
			rut=self.formato_rut(self.entryRutRepresentante.get_text().lower())
			if self.es_rut(rut):
					self.entryRutRepresentante.set_text(rut)
			else:
					self.entryRutRepresentante.set_text("")
