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
import gtk
import re
from gtk import TRUE, FALSE
from calendario import *
from prestamos import *
from dialogo_error import DialogoError
from types import StringType
from descuento_trabajador import *
import time
import string

class IngresarSeleccionar(GladeConnect):
	"Agregar Comentario"
	
	def __init__(self,cursor,rut_empresa_actual):
		GladeConnect.__init__(self, "glade/ingresarseleccionar.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre= None
		self.hermano=None
		self.rut_empresa_actual=rut_empresa_actual
		self.activo=0
		#poniendo no editable a las cajas
		self.entryNombres.set_sensitive(False)
		self.entryApellidoPaterno.set_sensitive(False)
		self.entryApellidoMaterno.set_sensitive(False)
		self.entryRutTrabajador.set_sensitive(False)
		self.entryFechaNacimiento.set_sensitive(False)
		self.comboboxentrySexo.set_sensitive(False)
		self.comboboxentrySexo.child.set_sensitive(False)
		self.comboboxentryNacionalidad.set_sensitive(False)
		self.comboboxentryNacionalidad.child.set_sensitive(False)
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(False)
		self.toolbuttonAdelante.set_sensitive(False)
		self.toolbuttonCalendario.set_sensitive(False)
		#pone el foco en codigo
		self.entryNombres.grab_focus()
		#metodo para treeview
		self.define_vista()
		self.crea_modelo()
		self.lista_datos()
		
		
	def define_vista(self):
		
		lbl = unicode('R.U.T. Trabajador')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=0)
		self.treeviewTrabajadores.append_column(column)
		
		lbl = unicode('Apellido Paterno')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=1)
		self.treeviewTrabajadores.append_column(column)
		
		lbl = unicode('Apellido Materno')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=2)
		self.treeviewTrabajadores.append_column(column)
		
		lbl = unicode('Nombres')
		column = gtk.TreeViewColumn(lbl.encode('utf-8'), gtk.CellRendererText(), text=3)
		self.treeviewTrabajadores.append_column(column)
		

	def crea_modelo(self):
		self.modelo = gtk.ListStore(str, str, str, str)
		self.treeviewTrabajadores.set_model(self.modelo)
		
	def lista_datos(self):
		self.modelo.clear()
		
		sql="""SELECT t.rut_trabajador,t.apellido_paterno_trabajador, 
			   t.apellido_materno_trabajador,t.nombres_trabajador 
			   FROM trabajador t, trabaja
			   WHERE t.rut_trabajador=trabaja.rut_trabajador 
			   and trabaja.rut_empresa='%s'
			   ORDER BY t.apellido_paterno_trabajador, t.apellido_materno_trabajador
			"""%(self.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		for i in r:
			self.modelo.append(i)
		
	def on_comboboxentryNacionalidad_changed(self,combo=None):
		model_aux = self.comboboxentryNacionalidad.get_model()
		active = self.comboboxentryNacionalidad.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryNacionalidad.child.set_text(elemento)
		if elemento=='OTRA':
			self.comboboxentryNacionalidad.child.set_sensitive(True)
			self.comboboxentryNacionalidad.child.grab_focus()
		else:
			self.comboboxentryNacionalidad.child.set_sensitive(False)
			
		return

	
	
	def on_treeviewTrabajadores_row_activated(self, tree, row, column):
		self.activo=1
		if len(self.padre.wins) and self.padre.wins.has_key("Fin ingresar trabajador"):
			self.padre.notebookMain.remove_page(3)
			del self.padre.wins["Fin ingresar trabajador"]

		self.pk_trabajador=(self.modelo[row][0])
		self.entryNombres.set_text(self.modelo[row][3])
		self.entryApellidoPaterno.set_text(self.modelo[row][1])
		self.entryApellidoMaterno.set_text(self.modelo[row][2])
		self.entryRutTrabajador.set_text(self.modelo[row][0])
		
		sql="""SELECT t.codigo_direccion,
		t.fecha_nacimiento_trabajor,
		t.sexo_trabajador,
		t.nacionalidad_trabajador,
		t.cargo_trabajador,
		t.fecha_ingreso_trabajador,
		t.tramo_carga_trabajador,
		d.codigo_direccion,
		d.nombre_comuna,
		d.nombre_calle_direccion,
		d.numero_direccion,
		d.block_direccion,
		d.departamento_direccion,
		a.codigo_antecedente_liquidacion,
		a.nombre_compania_seguro,
		a.nombre_salud,
		a.rut_trabajador,
		a.nombre_caja_compensacion,
		a.nombre_afp,
		a.sueldo_base,
		a.factor_hora_extras,
		a.colacion,
		a.movilizacion,
		a.numero_cargas,
		a.cargas_retroactivas,
		a.valor_total,
		a.afp_tipo_afiliado,
		a.ahorro_voluntario,
		a.seguro_cesantia,
		a.seguro_cesantia_porcen,
		a.adicional_pactado,
		a.monto_adicional_pactado_uf,
		a.posee_seguro_vida_c_s,
		a.s_v_c_numerocuota,
		a.s_v_c_s_valor,
		a.leasing_rut_codigo,
		a.leasing_numero_cuenta,
		a.leasing_numero_cuota,
		a.leasing_aporteuf_remuneracion,
		a.posee_s_v_c_c,
		a.s_v_c_c_numero_cuota,
		a.s_v_c_c_valor, 
		t.tipo_contrato
		FROM trabajador t, direccion d, localidad l,
		antecedente_liquidacion a
		WHERE t.codigo_direccion=d.codigo_direccion and
		t.rut_trabajador=a.rut_trabajador and
		t.rut_trabajador='%s'
		ORDER BY t.apellido_paterno_trabajador, t.apellido_materno_trabajador, 
		t.nombres_trabajador
		"""%(self.pk_trabajador)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()

		self.entryFechaNacimiento.set_text(r[0][1].strftime('%Y-%m-%d'))
		self.toolbuttonCalendario.set_sensitive(True)
		self.comboboxentrySexo.child.set_text(r[0][2])
		self.comboboxentrySexo.set_sensitive(True)
		self.comboboxentryNacionalidad.child.set_text(r[0][3])
		self.comboboxentryNacionalidad.set_sensitive(True)
		self.padre.antecedentespersonales.comboboxentryTipoContrato.child.set_text(r[0][42])
		self.padre.antecedentespersonales.comboboxentryCargo.child.set_text(r[0][4])
		self.padre.antecedentespersonales.entryFechaIngreso.set_text(r[0][5].strftime('%Y-%m-%d'))
		self.padre.antecedentespersonales.entryCalle.set_text(r[0][9])
		self.padre.antecedentespersonales.entryNumero.set_text(str(r[0][10]))
		if not (r[0][11]==None or r[0][11]==" "):
			self.padre.antecedentespersonales.radiobuttonDepartamentoSi.set_active(True)
			self.padre.antecedentespersonales.entryBlock.set_text(r[0][11])
			self.padre.antecedentespersonales.entryDepartamento.set_text(str(r[0][12]))
		self.padre.antecedentespersonales.comboboxentryComuna.child.set_text(r[0][8])
		
		self.padre.antecedentesliquidacion.comboboxentryAfp.child.set_text(r[0][18])
		self.padre.antecedentesliquidacion.comboboxentryTipoAfiliado.child.set_text(r[0][26])
		self.padre.antecedentesliquidacion.entrySueldoBase.set_text(str(r[0][19]))
		self.padre.antecedentesliquidacion.entryFactorHorasExtras.set_text(str(r[0][20]))
		self.padre.antecedentesliquidacion.entryColacion.set_text(str(r[0][21]))
		self.padre.antecedentesliquidacion.entryMovilizacion.set_text(str(r[0][22]))
		self.padre.antecedentesliquidacion.entryNumeroCargas.set_text(str(r[0][23]))
		model_aux = self.padre.antecedentesliquidacion.comboboxentryTramoCargas.get_model()
		elemento= model_aux[r[0][6]-1][0]
		
		self.padre.antecedentesliquidacion.comboboxentryTramoCargas.child.set_text(elemento)
		self.padre.antecedentesliquidacion.entryCargasRetroactivas.set_text(str(r[0][24]))
		self.padre.antecedentesliquidacion.entryValorTotal.set_text(str(r[0][25]))
		self.padre.antecedentesliquidacion.entryAhorroVoluntario.set_text(str(r[0][27]))
		self.padre.antecedentesliquidacion.comboboxentrySalud.child.set_text(r[0][15])
		if r[0][15]=='FONASA':
			self.padre.antecedentesliquidacion.toolbuttonPrestamoSalud.set_sensitive(True)
			self.padre.antecedentesliquidacion.frameAdicionalPactado.hide()
		else:
			self.padre.antecedentesliquidacion.toolbuttonPrestamoSalud.set_sensitive(False)
		
		if r[0][30]=='SI':
			self.padre.antecedentesliquidacion.radiobuttonPoseeSi.set_active(True)
			self.padre.antecedentesliquidacion.entryCantidadUF.set_text(str(r[0][31]))
		
		if r[0][32]=='SI':
			self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaSi.set_active(True)
			self.padre.antecedentesliquidacion.comboboxentrySeleccionarCompania.child.set_text(r[0][14])
			self.padre.antecedentesliquidacion.entryNumeroCuotaSeguro.set_text(str(r[0][33]))
			self.padre.antecedentesliquidacion.entryValorSeguro.set_text(str(r[0][34]))

		if r[0][28]=='SI':
			self.padre.antecedentesliquidacion.radiobuttonSeguroCesantiaSi.set_active(True)
			self.padre.antecedentesliquidacion.entryPorcientoSeguroDesempleo.set_text(str(r[0][29]))
			
		if not (r[0][35]==None or r[0][35]==" "):
			self.padre.antecedentesliquidacion.radiobuttonLeasingSi.set_active(True)
			self.padre.antecedentesliquidacion.entryRutCodigoInterno.set_text(r[0][35])
			self.padre.antecedentesliquidacion.entryNumeroCuenta.set_text(str(r[0][36]))
			self.padre.antecedentesliquidacion.entryNumeroCuota.set_text(str(r[0][37]))
			self.padre.antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_text(str(r[0][38]))

		if r[0][39]=='SI':
			self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaSi.set_active(True)
			self.padre.antecedentesliquidacion.comboboxentrySeleccionarCaja.child.set_text(r[0][17])
			self.padre.antecedentesliquidacion.entryCajaNumeroCuota.set_text(str(r[0][40]))
			self.padre.antecedentesliquidacion.entryCajaValor.set_text(str(r[0][41]))

		self.toolbuttonNuevo.set_sensitive(False)
		self.toolbuttonQuitar.set_sensitive(True)
		self.toolbuttonAdelante.set_sensitive(True)
		self.toolbuttonActualizar.set_sensitive(True)
		self.padre.antecedentespersonales.toolbuttonAdelante.set_sensitive(True)
		self.padre.antecedentespersonales.toolbuttonAtras.set_sensitive(True)
		self.padre.antecedentesliquidacion.toolbuttonAdelante.set_sensitive(True)
		self.padre.antecedentesliquidacion.toolbuttonAtras.set_sensitive(True)
		
		#Poniendo editable a las cajas 
		self.entryRutTrabajador.set_sensitive(True)
		self.entryApellidoPaterno.set_sensitive(True)
		self.entryApellidoMaterno.set_sensitive(True)
		self.entryNombres.set_sensitive(True)
		
		self.pk_antecedenteliquidacion=r[0][13]
		self.pk_direccion=r[0][7]
		self.toolbuttonNuevo.set_sensitive(True)
		self.padre.antecedentesliquidacion.toolbuttonPrestamoCaja.set_sensitive(True)
		self.padre.antecedentesliquidacion.toolbuttonPrestamoEmpresa.set_sensitive(True)
		self.padre.antecedentesliquidacion.toolbuttonDescuento.set_sensitive(True)
		
	def on_toolbuttonNuevo_clicked(self, toolbuttonNuevo=None):
		self.padre._nueva_pagina(self.padre.finingresartrabajador.vboxFinIngresarTrabajador,"Fin ingresar trabajador")

		#poniendo editable a las cajas 
		self.entryNombres.set_sensitive(True)
		self.entryApellidoPaterno.set_sensitive(True)
		self.entryApellidoMaterno.set_sensitive(True)
		self.entryRutTrabajador.set_sensitive(True)
		self.entryFechaNacimiento.set_sensitive(False)
		self.comboboxentrySexo.set_sensitive(True)
		self.comboboxentryNacionalidad.set_sensitive(True)
		
		#poniendo disponibles a los botones que corresponden
		self.toolbuttonActualizar.set_sensitive(False)
		self.toolbuttonAdelante.set_sensitive(True)
		self.toolbuttonCalendario.set_sensitive(True)
		
		#borra el contenido de las cajas
		self.entryNombres.set_text("")
		self.entryApellidoPaterno.set_text("")
		self.entryApellidoMaterno.set_text("")
		self.entryRutTrabajador.set_text("")
		self.entryFechaNacimiento.set_text("")
		self.comboboxentrySexo.child.set_text("")
		self.comboboxentryNacionalidad.child.set_text("")

		#foco en en rut de trabajador
		self.entryNombres.grab_focus()
		#poniendo no editable
		self.padre.antecedentespersonales.comboboxentryTipoContrato.set_sensitive(False)
		self.padre.antecedentespersonales.comboboxentryCargo.set_sensitive(False)
		self.padre.antecedentespersonales.entryFechaIngreso.set_sensitive(False)
		self.padre.antecedentespersonales.entryCalle.set_sensitive(False)
		self.padre.antecedentespersonales.radiobuttonDepartamentoNo.set_sensitive(False)
		self.padre.antecedentespersonales.radiobuttonDepartamentoSi.set_sensitive(False)
		self.padre.antecedentespersonales.radiobuttonDepartamentoNo.set_active(True)
		self.padre.antecedentespersonales.entryNumero.set_sensitive(False)
		self.padre.antecedentespersonales.entryBlock.set_sensitive(False)
		self.padre.antecedentespersonales.entryDepartamento.set_sensitive(False)
		self.padre.antecedentespersonales.entryCiudad.set_sensitive(False)
		self.padre.antecedentespersonales.comboboxentryComuna.set_sensitive(False)
		self.padre.antecedentespersonales.entryRegion.set_sensitive(False)
		#borrando contenido
		self.padre.antecedentespersonales.comboboxentryTipoContrato.child.set_text("")
		self.padre.antecedentespersonales.comboboxentryCargo.child.set_text("")
		self.padre.antecedentespersonales.entryFechaIngreso.set_text("")
		self.padre.antecedentespersonales.entryCalle.set_text("")
		self.padre.antecedentespersonales.entryNumero.set_text("")
		self.padre.antecedentespersonales.entryBlock.set_text("")
		self.padre.antecedentespersonales.entryDepartamento.set_text("")
		self.padre.antecedentespersonales.comboboxentryComuna.child.set_text("")
		#poniendo no disponibles botones que corresponden
		self.padre.antecedentespersonales.toolbuttonAtras.set_sensitive(False)
		self.padre.antecedentespersonales.toolbuttonAdelante.set_sensitive(False)
		#poniendo no editable antecedetes liquidacion
		self.padre.antecedentesliquidacion.entrySueldoBase.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryFactorHorasExtras.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryColacion.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryMovilizacion.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryNumeroCargas.set_sensitive(False)
		self.padre.antecedentesliquidacion.comboboxentryTramoCargas.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryCargasRetroactivas.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryValorTotal.set_sensitive(False)
		self.padre.antecedentesliquidacion.comboboxentryAfp.set_sensitive(False)
		self.padre.antecedentesliquidacion.comboboxentryTipoAfiliado.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryAhorroVoluntario.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonSeguroCesantiaNo.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonSeguroCesantiaSi.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonSeguroCesantiaNo.set_active(True)
		self.padre.antecedentesliquidacion.radiobuttonLeasingNo.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonLeasingSi.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonLeasingNo.set_active(True)
		self.padre.antecedentesliquidacion.entryPorcientoSeguroDesempleo.set_sensitive(False)
		self.padre.antecedentesliquidacion.comboboxentrySalud.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonPoseeNo.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonPoseeSi.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonPoseeNo.set_active(True)
		self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaNo.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaSi.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaNo.set_active(True)
		self.padre.antecedentesliquidacion.comboboxentrySeleccionarCompania.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryNumeroCuotaSeguro.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryValorSeguro.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaNo.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaSi.set_sensitive(False)
		self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaNo.set_active(True)
		self.padre.antecedentesliquidacion.entryRutCodigoInterno.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryNumeroCuenta.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryNumeroCuota.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_sensitive(False)
		self.padre.antecedentesliquidacion.comboboxentrySeleccionarCaja.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryCajaNumeroCuota.set_sensitive(False)
		self.padre.antecedentesliquidacion.entryCajaValor.set_sensitive(False)
		#borrando contenido
		self.padre.antecedentesliquidacion.comboboxentryAfp.child.set_text("")
		self.padre.antecedentesliquidacion.comboboxentryTipoAfiliado.child.set_text("")
		self.padre.antecedentesliquidacion.entrySueldoBase.set_text("")
		self.padre.antecedentesliquidacion.entryFactorHorasExtras.set_text("0")
		self.padre.antecedentesliquidacion.entryColacion.set_text("")
		self.padre.antecedentesliquidacion.entryMovilizacion.set_text("")
		self.padre.antecedentesliquidacion.entryNumeroCargas.set_text("")
		self.padre.antecedentesliquidacion.comboboxentryTramoCargas.child.set_text("")
		self.padre.antecedentesliquidacion.entryCargasRetroactivas.set_text("0")
		self.padre.antecedentesliquidacion.entryValorTotal.set_text("")
		self.padre.antecedentesliquidacion.comboboxentryAfp.child.set_text("")
		self.padre.antecedentesliquidacion.comboboxentryTipoAfiliado.child.set_text("")
		self.padre.antecedentesliquidacion.entryAhorroVoluntario.set_text("0")
		self.padre.antecedentesliquidacion.comboboxentrySalud.child.set_text("")
		self.padre.antecedentesliquidacion.comboboxentrySeleccionarCompania.child.set_text("")
		self.padre.antecedentesliquidacion.entryNumeroCuotaSeguro.set_text("")
		self.padre.antecedentesliquidacion.entryValorSeguro.set_text("")
		self.padre.antecedentesliquidacion.entryPorcientoSeguroDesempleo.set_text("")
		self.padre.antecedentesliquidacion.entryRutCodigoInterno.set_text("")
		self.padre.antecedentesliquidacion.entryNumeroCuenta.set_text("")
		self.padre.antecedentesliquidacion.entryNumeroCuota.set_text("")
		self.padre.antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_text("")
		self.padre.antecedentesliquidacion.comboboxentrySeleccionarCaja.child.set_text("")
		self.padre.antecedentesliquidacion.entryCajaNumeroCuota.set_text("")
		self.padre.antecedentesliquidacion.entryCajaValor.set_text("")
		#poniendo no disponibles a los botones que corresponden
		self.padre.antecedentesliquidacion.toolbuttonAtras.set_sensitive(False)
		self.padre.antecedentesliquidacion.toolbuttonAdelante.set_sensitive(False)
		self.padre.antecedentesliquidacion.toolbuttonPrestamoCaja.set_sensitive(False)
		self.padre.antecedentesliquidacion.toolbuttonPrestamoEmpresa.set_sensitive(False)
		
	
	def on_toolbuttonAdelante_clicked(self, toolbuttonAdelante=None):
		self.padre.notebookMain.next_page()
		self.hermano.comboboxentryTipoContrato.set_sensitive(True)
		self.hermano.comboboxentryCargo.set_sensitive(True)
		self.hermano.entryCalle.set_sensitive(True)
		self.hermano.entryNumero.set_sensitive(True)
		self.hermano.comboboxentryComuna.set_sensitive(True)
		self.hermano.radiobuttonDepartamentoNo.set_sensitive(True)
		self.hermano.radiobuttonDepartamentoSi.set_sensitive(True)
		#botones sensibles
		self.hermano.toolbuttonAtras.set_sensitive(True)
		self.hermano.toolbuttonAdelante.set_sensitive(True)
		self.hermano.toolbuttonCalendario.set_sensitive(True)
		
	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizar=None):
		sql	="""
			 SELECT * 
			 FROM localidad WHERE nombre_comuna='%s'
			 """%(self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper())
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		try:
			if len(r)==0:		
				sql ="""
					 INSERT INTO localidad
					 VALUES ('%s','%s','%s')
					 """%(
					 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
					 self.padre.antecedentespersonales.entryCiudad.get_text().upper(),
					 self.padre.antecedentespersonales.entryRegion.get_text().upper()
					 )
				self.cursor.execute(sql)
				if self.padre.antecedentespersonales.radiobuttonDepartamentoSi.get_active():
					sql ="""
						 UPDATE direccion
						 SET
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s',block_direccion='%s',
						 departamento_direccion='%s'
						 WHERE codigo_direccion='%s'
						 """%(
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text(),
						 self.padre.antecedentespersonales.entryBlock.get_text().upper(),
						 self.padre.antecedentespersonales.entryDepartamento.get_text(),
						 self.pk_direccion
						 )
					self.cursor.execute(sql)
				else:
					sql ="""
						 UPDATE direccion
						 SET
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s',block_direccion=' ',
						 departamento_direccion='0'
						 WHERE codigo_direccion='%s'
						 """%(
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text(),
						 self.pk_direccion
						 )
					self.cursor.execute(sql)
			else:
				if self.padre.antecedentespersonales.radiobuttonDepartamentoSi.get_active():
					sql ="""
						 UPDATE direccion
						 SET
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s',block_direccion='%s',
						 departamento_direccion='%s'
						 WHERE codigo_direccion='%s'
						 """%(
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text(),
						 self.padre.antecedentespersonales.entryBlock.get_text().upper(),
						 self.padre.antecedentespersonales.entryDepartamento.get_text(),
						 self.pk_direccion
						 )
					self.cursor.execute(sql)
				else:
					sql ="""
						 UPDATE direccion
						 SET
						 nombre_comuna='%s',nombre_calle_direccion='%s',
						 numero_direccion='%s',block_direccion=' ',
						 departamento_direccion='0'
						 WHERE codigo_direccion='%s'
						 """%(
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text(),
						 self.pk_direccion
						 )
					self.cursor.execute(sql)
				
			trabajador={}
			trabajador["rut_trabajador"]=(self.padre.ingresarseleccionar.entryRutTrabajador.get_text().upper())
			if self.padre.antecedentespersonales.radiobuttonDepartamentoSi.get_active():
				sql	="""
					 SELECT codigo_direccion 
					 FROM direccion WHERE
					 nombre_calle_direccion='%s' and
					 numero_direccion='%s' and
					 block_direccion='%s' and
					 departamento_direccion='%s'
					 """%(
					 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
					 self.padre.antecedentespersonales.entryNumero.get_text(),
					 self.padre.antecedentespersonales.entryBlock.get_text().upper(),
					 self.padre.antecedentespersonales.entryDepartamento.get_text() 
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
					 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
					 self.padre.antecedentespersonales.entryNumero.get_text(),
					 )
				self.cursor.execute(sql)
				r=self.cursor.fetchall()
				
			trabajador["codigo_direccion"]=(str(r[0][0]))
			trabajador["apellido_paterno_trabajador"]=(self.padre.ingresarseleccionar.entryApellidoPaterno.get_text().upper())
			trabajador["apellido_materno_trabajador"]=(self.padre.ingresarseleccionar.entryApellidoMaterno.get_text().upper())
			trabajador["nombres_trabajador"]=(self.padre.ingresarseleccionar.entryNombres.get_text().upper())
			trabajador["fecha_nacimiento_trabajor"]=(self.padre.ingresarseleccionar.entryFechaNacimiento.get_text())	
			trabajador["sexo_trabajador"]=(self.padre.ingresarseleccionar.comboboxentrySexo.child.get_text().upper())
			trabajador["nacionalidad_trabajador"]=(self.padre.ingresarseleccionar.comboboxentryNacionalidad.child.get_text().upper())
			trabajador["cargo_trabajador"]=(self.padre.antecedentespersonales.comboboxentryCargo.child.get_text().upper())
			trabajador["fecha_ingreso_trabajador"]=(self.padre.antecedentespersonales.entryFechaIngreso.get_text())	
			auxiliar=self.padre.antecedentesliquidacion.comboboxentryTramoCargas.child.get_text()
			trabajador["tramo_carga_trabajador"]=(auxiliar[0])
			trabajador["tipo_contrato"]=(self.padre.antecedentespersonales.comboboxentryTipoContrato.child.get_text())
			
			sql ="""
				 UPDATE trabajador
				 SET """+",".join(["%s='%s'"%(n1,n2) for n1,n2 in trabajador.iteritems()])+"""
				 WHERE rut_trabajador='%s'
				 """%(self.pk_trabajador)
				 
			self.cursor.execute(sql)
			#antecedente liquidacion
			antecedente_liquidacion={}
			antecedente_liquidacion["rut_empresa"]=(self.padre.rut_empresa_actual)
			if not self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaNo.get_active():
				antecedente_liquidacion["nombre_compania_seguro"]=(self.padre.antecedentesliquidacion.comboboxentrySeleccionarCompania.child.get_text().upper())
				
			antecedente_liquidacion["nombre_salud"]=(self.padre.antecedentesliquidacion.comboboxentrySalud.child.get_text().upper())
			antecedente_liquidacion["rut_trabajador"]=(self.padre.ingresarseleccionar.entryRutTrabajador.get_text().upper())
			
			if self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaSi.get_active():
				antecedente_liquidacion["nombre_caja_compensacion"]=(self.padre.antecedentesliquidacion.comboboxentrySeleccionarCaja.child.get_text().upper())

			antecedente_liquidacion["nombre_afp"]=(self.padre.antecedentesliquidacion.comboboxentryAfp.child.get_text().upper())
			antecedente_liquidacion["sueldo_base"]=(self.padre.antecedentesliquidacion.entrySueldoBase.get_text())
			antecedente_liquidacion["factor_hora_extras"]=(self.padre.antecedentesliquidacion.entryFactorHorasExtras.get_text())
			antecedente_liquidacion["colacion"]=(self.padre.antecedentesliquidacion.entryColacion.get_text())
			antecedente_liquidacion["movilizacion"]=(self.padre.antecedentesliquidacion.entryMovilizacion.get_text())
			antecedente_liquidacion["numero_cargas"]=(self.padre.antecedentesliquidacion.entryNumeroCargas.get_text())
			antecedente_liquidacion["cargas_retroactivas"]=(self.padre.antecedentesliquidacion.entryCargasRetroactivas.get_text())
			antecedente_liquidacion["valor_total"]=(self.padre.antecedentesliquidacion.entryValorTotal.get_text())
			antecedente_liquidacion["afp_tipo_afiliado"]=(self.padre.antecedentesliquidacion.comboboxentryTipoAfiliado.child.get_text())
			antecedente_liquidacion["ahorro_voluntario"]=(self.padre.antecedentesliquidacion.entryAhorroVoluntario.get_text())
			
			if not self.padre.antecedentesliquidacion.radiobuttonSeguroCesantiaNo.get_active():
				antecedente_liquidacion["seguro_cesantia"]=("SI")
				antecedente_liquidacion["seguro_cesantia_porcen"]=(self.padre.antecedentesliquidacion.entryPorcientoSeguroDesempleo.get_text())
			else:
				antecedente_liquidacion["seguro_cesantia"]=("NO")
				antecedente_liquidacion["seguro_cesantia_porcen"]=(0)
						
			if not self.padre.antecedentesliquidacion.radiobuttonPoseeNo.get_active():
				antecedente_liquidacion["adicional_pactado"]=("SI")
				antecedente_liquidacion["monto_adicional_pactado_uf"]=(self.padre.antecedentesliquidacion.entryCantidadUF.get_text())
			else:
				antecedente_liquidacion["adicional_pactado"]=("NO")
				antecedente_liquidacion["monto_adicional_pactado_uf"]=(0)
			
			if self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaNo.get_active():
				antecedente_liquidacion["posee_seguro_vida_c_s"]=("NO")
				antecedente_liquidacion["s_v_c_numerocuota"]=(0)
				antecedente_liquidacion["s_v_c_s_valor"]=(0)
			else:
				antecedente_liquidacion["posee_seguro_vida_c_s"]=("SI")
				antecedente_liquidacion["s_v_c_numerocuota"]=(self.padre.antecedentesliquidacion.entryNumeroCuotaSeguro.get_text())
				antecedente_liquidacion["s_v_c_s_valor"]=(self.padre.antecedentesliquidacion.entryValorSeguro.get_text())
			
			if self.padre.antecedentesliquidacion.radiobuttonLeasingSi.get_active():
				antecedente_liquidacion["leasing_rut_codigo"]=(self.padre.antecedentesliquidacion.entryRutCodigoInterno.get_text())
				antecedente_liquidacion["leasing_numero_cuenta"]=(self.padre.antecedentesliquidacion.entryNumeroCuenta.get_text())
				antecedente_liquidacion["leasing_numero_cuota"]=(self.padre.antecedentesliquidacion.entryNumeroCuota.get_text())
				antecedente_liquidacion["leasing_aporteuf_remuneracion"]=(self.padre.antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.get_text())
			else:
				antecedente_liquidacion["leasing_rut_codigo"]=(" ")
				antecedente_liquidacion["leasing_numero_cuenta"]=(0)
				antecedente_liquidacion["leasing_numero_cuota"]=(0)
				antecedente_liquidacion["leasing_aporteuf_remuneracion"]=(0)
			
			if self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaNo.get_active():
				antecedente_liquidacion["posee_s_v_c_c"]=("NO")
				antecedente_liquidacion["s_v_c_c_numero_cuota"]=(0)
				antecedente_liquidacion["s_v_c_c_valor"]=(0)
			
			else:
				antecedente_liquidacion["posee_s_v_c_c"]=("SI")
				antecedente_liquidacion["s_v_c_c_numero_cuota"]=(self.padre.antecedentesliquidacion.entryCajaNumeroCuota.get_text())
				antecedente_liquidacion["s_v_c_c_valor"]=(self.padre.antecedentesliquidacion.entryCajaValor.get_text())
			
			sql="""UPDATE antecedente_liquidacion 
			SET """+",".join(["%s='%s'" %(n1,n2) for n1,n2 in antecedente_liquidacion.iteritems()])+"""
			WHERE
			codigo_antecedente_liquidacion='%s'
			"""%(self.pk_antecedenteliquidacion)			
			self.cursor.execute(sql)
			self.padre.cnx.commit()
		except:
			string = StringType(sys.exc_info()[1])
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self.padre
			self.padre.vbox1.set_sensitive(False)
			return
		self.on_toolbuttonNuevo_clicked() 
	
	def on_toolbuttonQuitar_clicked(self, toolbuttonQuitar=None):
		print "quitar"

	def on_toolbuttonCalendario_clicked(self, toolCalendaraio=None):
		a=Calendario(1)
		a.padre=self.padre
		a.windowCalendario.show()

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

	def on_entryRutTrabajador_focus_out_event(self, widget=None, eventda=None):
			rut=self.formato_rut(self.entryRutTrabajador.get_text().lower())
			if self.es_rut(rut):
					self.entryRutTrabajador.set_text(rut)
			else:
					self.entryRutTrabajador.set_text("")
			


class AntecedentesPersonales(GladeConnect):
	"agregar comentario"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/antecedentespersonales.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.hermano=None
		#poniendo no editable a las cajas
		self.comboboxentryTipoContrato.set_sensitive(False)
		self.comboboxentryTipoContrato.child.set_sensitive(False)
		self.comboboxentryCargo.set_sensitive(False)
		self.comboboxentryCargo.child.set_sensitive(False)
		self.entryFechaIngreso.set_sensitive(False)
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
		
		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAtras.set_sensitive(False)
		self.toolbuttonAdelante.set_sensitive(False)
		self.toolbuttonCalendario.set_sensitive(False)
		

	def on_toolbuttonAtras_clicked(self, toolbuttonAtras=None):
		self.padre.notebookMain.prev_page()
	
	def on_toolbuttonAdelante_clicked(self, toolbuttonAdelante=None):
		self.padre.notebookMain.next_page()
		#poniendo editable a las cajas
		
		#antecedentes imponibles
		self.hermano.entrySueldoBase.set_sensitive(True)
		self.hermano.entryFactorHorasExtras.set_sensitive(True)
		
		#antecedentes no imponibles
		self.hermano.entryColacion.set_sensitive(True)
		self.hermano.entryMovilizacion.set_sensitive(True)
		self.hermano.entryNumeroCargas.set_sensitive(True)
		self.hermano.comboboxentryTramoCargas.set_sensitive(True)
		self.hermano.entryCargasRetroactivas.set_sensitive(True)
		self.hermano.entryValorTotal.set_sensitive(True)
		
		#antecedentes descuentos
		self.hermano.comboboxentryAfp.set_sensitive(True)
		self.hermano.comboboxentryTipoAfiliado.set_sensitive(True)
		self.hermano.entryAhorroVoluntario.set_sensitive(True)
		self.hermano.comboboxentrySalud.set_sensitive(True)
		self.hermano.radiobuttonPoseeNo.set_sensitive(True)
		self.hermano.radiobuttonPoseeSi.set_sensitive(True)
		self.hermano.radiobuttonCompaniaSeguroVidaNo.set_sensitive(True)
		self.hermano.radiobuttonCompaniaSeguroVidaSi.set_sensitive(True)
		self.hermano.radiobuttonLeasingNo.set_sensitive(True)
		self.hermano.radiobuttonLeasingSi.set_sensitive(True)
		self.hermano.radiobuttonCajaSeguroVidaNo.set_sensitive(True)
		self.hermano.radiobuttonCajaSeguroVidaSi.set_sensitive(True)
		#botones sensibles
		self.hermano.toolbuttonAtras.set_sensitive(True)
		self.hermano.toolbuttonAdelante.set_sensitive(True)
	
		#foco
		self.hermano.entrySueldoBase.grab_focus()
		
	def on_toolbuttonCalendario_clicked(self, toolbuttonCalendario=None):
		a=Calendario(2)
		a.padre=self.padre
		a.windowCalendario.show()
		
		
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

	def on_comboboxentryTipoContrato_changed(self,combo=None):
		self.on_entryFechaIngreso_changed()
		return
	
	def on_entryFechaIngreso_changed(self, entry=None):
		mytime = time.mktime((2002,8,01, 0, 0, 0, 0, 0,-1))
		fecha_seguro=time.strftime('%Y-%m-%d',time.localtime(mytime))
		if (not self.entryFechaIngreso.get_text()=='') and (not self.comboboxentryTipoContrato.child.get_text()==''):
			string_fecha=self.entryFechaIngreso.get_text().split("-")
			mytime = time.mktime((int(string_fecha[0]),int(string_fecha[1]),int(string_fecha[2]), 0, 0, 0, 0, 0,-1))
			fecha_trabajador=time.strftime('%Y-%m-%d',time.localtime(mytime))
			if fecha_trabajador >= fecha_seguro:
				self.hermano.radiobuttonSeguroCesantiaSi.set_active(True)
				if self.comboboxentryTipoContrato.child.get_text()=='PLAZO FIJO':
					self.hermano.entryPorcientoSeguroDesempleo.set_text("0.0")
					self.hermano.entryPorcientoSeguroDesempleo.set_sensitive(False)
					self.hermano.radiobuttonSeguroCesantiaNo.set_sensitive(False)
				elif self.comboboxentryTipoContrato.child.get_text()=='PLAZO INDEFINIDO':
					self.hermano.entryPorcientoSeguroDesempleo.set_text("0.06")
					self.hermano.entryPorcientoSeguroDesempleo.set_sensitive(False)
					self.hermano.radiobuttonSeguroCesantiaNo.set_sensitive(False)
			else:
				self.hermano.radiobuttonSeguroCesantiaNo.set_sensitive(True)
				self.hermano.radiobuttonSeguroCesantiaSi.set_sensitive(True)
				self.hermano.radiobuttonSeguroCesantiaNo.set_active(True)
		return
		
class AntecedentesLiquidacion(GladeConnect):
	"agregar comentario"
	
	def __init__(self,cursor,fecha):
		GladeConnect.__init__(self, "glade/antecedentesliquidacion.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.hermano= None
		self.fecha=fecha
		self.regexp=re.compile("[0-9]+")
		#poniendo no editable a las cajas
		#antecedentes imponibles
		self.entrySueldoBase.set_sensitive(False)
		self.entryFactorHorasExtras.set_sensitive(False)
		
		#antecedentes no imponibles
		self.entryColacion.set_sensitive(False)
		self.entryMovilizacion.set_sensitive(False)
		self.entryNumeroCargas.set_sensitive(False)
		self.comboboxentryTramoCargas.set_sensitive(False)
		self.comboboxentryTramoCargas.child.set_sensitive(False)
		self.entryCargasRetroactivas.set_sensitive(False)
		self.entryValorTotal.set_sensitive(False)
		
		#antecedentes descuentos
		self.comboboxentryAfp.set_sensitive(False)
		self.comboboxentryAfp.child.set_sensitive(False)
		self.comboboxentryTipoAfiliado.set_sensitive(False)
		self.comboboxentryTipoAfiliado.child.set_sensitive(False)
		self.entryAhorroVoluntario.set_sensitive(False)
		self.radiobuttonSeguroCesantiaNo.set_sensitive(False)
		self.radiobuttonSeguroCesantiaSi.set_sensitive(False)
		self.entryPorcientoSeguroDesempleo.set_sensitive(False)
		self.comboboxentrySalud.set_sensitive(False)
		self.comboboxentrySalud.child.set_sensitive(False)
		self.radiobuttonPoseeNo.set_sensitive(False)
		self.radiobuttonPoseeSi.set_sensitive(False)
		self.entryCantidadUF.set_sensitive(False)
		self.comboboxentrySeleccionarCompania.set_sensitive(False)
		self.comboboxentrySeleccionarCompania.child.set_sensitive(False)
		self.entryNumeroCuotaSeguro.set_sensitive(False)
		self.entryValorSeguro.set_sensitive(False)
		self.radiobuttonLeasingNo.set_sensitive(False)
		self.radiobuttonLeasingSi.set_sensitive(False)
		self.entryRutCodigoInterno.set_sensitive(False)
		self.entryNumeroCuenta.set_sensitive(False)
		self.entryNumeroCuota.set_sensitive(False)
		self.entryAporteUFPorcentajeRemuneracion.set_sensitive(False)
		self.radiobuttonCompaniaSeguroVidaNo.set_sensitive(False)
		self.radiobuttonCompaniaSeguroVidaSi.set_sensitive(False)
		self.radiobuttonCajaSeguroVidaNo.set_sensitive(False)
		self.radiobuttonCajaSeguroVidaSi.set_sensitive(False)
		self.comboboxentrySeleccionarCaja.set_sensitive(False)
		self.comboboxentrySeleccionarCaja.child.set_sensitive(False)
		self.entryCajaNumeroCuota.set_sensitive(False)
		self.entryCajaValor.set_sensitive(False)

		#poniendo no disponibles a los botones que corresponden
		self.toolbuttonAtras.set_sensitive(False)
		self.toolbuttonAdelante.set_sensitive(False)
		self.toolbuttonPrestamoCaja.set_sensitive(False)
		self.toolbuttonPrestamoEmpresa.set_sensitive(False)
		self.toolbuttonPrestamoSalud.set_sensitive(False)
		self.toolbuttonDescuento.set_sensitive(False)
		
		#metodo para los comboboxentry afp
		self.crear_combos_modelo_afp()
		self.llenar_combos_afp()
		#metodo para los comboboxentry salud
		self.crear_combos_modelo_salud()
		self.llenar_combos_salud()
		#metodo para los comboboxentry carga
		self.crear_combos_modelo_carga()
		self.llenar_combos_carga()
		#metodo para los comboboxentry compania_seguro
		self.crear_combos_modelo_compania()
		self.llenar_combos_compania()
		#metodo para los comboboxentry caja compensacion
		self.crear_combos_modelo_caja()
		self.llenar_combos_caja()
		#pone el foco en codigo
		self.entrySueldoBase.grab_focus()

	def llenar_combos_carga(self):
		self.modelo_carga_familiar.clear()
		
		sql="""SELECT tramo_carga_familiar
			   FROM tramo_carga_familiar 
			"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if not len(r)==0:
			cadena=str(r[0][0])
			numeros=self.regexp.findall(cadena)
			resultado=[str(i) for i in numeros]
			
			a="1er Tramo ("+resultado[0]+" - "+resultado[1]+")"
			b="2do Tramo ("+resultado[3]+" - "+resultado[4]+")"
			c="3ro Tramo ("+resultado[6]+" - "+resultado[7]+")"
			d="4to Tramo ("+resultado[9]+" - "+resultado[10]+")"
			resultado=[]
			resultado.append([str(a)])
			resultado.append([str(b)])
			resultado.append([str(c)])
			resultado.append([str(d)])
			
			for i in resultado:
				self.modelo_carga_familiar.append(i)
			
		else:
			print "no existen tramos para carga familiar"
			
	def crear_combos_modelo_carga(self):
		self.modelo_carga_familiar= gtk.ListStore(str) 
		self.comboboxentryTramoCargas.set_model(self.modelo_carga_familiar)
		cell=gtk.CellRendererText()
		self.comboboxentryTramoCargas.pack_start(cell,True)
		self.comboboxentryTramoCargas.add_attribute(cell,'text',0)
		return
		
	def on_comboboxentryTramoCargas_changed(self,combo=None):
		model_aux = self.comboboxentryTramoCargas.get_model()
		active = self.comboboxentryTramoCargas.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryTramoCargas.child.set_text(elemento)
		sql="""SELECT tramo_carga_familiar
		FROM tramo_carga_familiar
		"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		indice=int(elemento[0])-1
		if not self.entryNumeroCargas.get_text()=='':
			self.entryValorTotal.set_text(str(int(self.entryNumeroCargas.get_text())*int(r[0][0][indice][2])))
		return

	def llenar_combos_compania(self):
		self.modelo_compania.clear()
		
		sql="""SELECT nombre_compania_seguro
			   FROM compania_seguro
			   ORDER BY nombre_compania_seguro
			"""
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if not len(r)==0:
			for i in r:
				self.modelo_compania.append(i)
		else:
			print "no existen companias"
			
	def crear_combos_modelo_compania(self):
		self.modelo_compania= gtk.ListStore(str) 
		self.comboboxentrySeleccionarCompania.set_model(self.modelo_compania)
		cell=gtk.CellRendererText()
		self.comboboxentrySeleccionarCompania.pack_start(cell,True)
		self.comboboxentrySeleccionarCompania.add_attribute(cell,'text',0)
		
		return

	def on_comboboxentrySeleccionarCompania_changed(self,combo=None):
		model_aux = self.comboboxentrySeleccionarCompania.get_model()
		active = self.comboboxentrySeleccionarCompania.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentrySeleccionarCompania.child.set_text(elemento)
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
		
		if not len(r)==0:
			for i in r:
				self.modelo_caja.append(i)
		else:
			print "no existen caja"
			
	def crear_combos_modelo_caja(self):
		self.modelo_caja= gtk.ListStore(str) 
		self.comboboxentrySeleccionarCaja.set_model(self.modelo_caja)
		cell=gtk.CellRendererText()
		self.comboboxentrySeleccionarCaja.pack_start(cell,True)
		self.comboboxentrySeleccionarCaja.add_attribute(cell,'text',0)
		return
		
	def on_comboboxentrySeleccionarCaja_changed(self,combo=None):
		model_aux = self.comboboxentrySeleccionarCaja.get_model()
		active = self.comboboxentrySeleccionarCaja.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentrySeleccionarCaja.child.set_text(elemento)
		return
	
	def llenar_combos_afp(self):
		self.modelo_afp.clear()
		
		sql	="""
			 SELECT nombre_afp
			 FROM afp
			 ORDER BY nombre_afp
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if not len(r)==0:
			for i in r:
				self.modelo_afp.append(i)
		else:
			print "no existen afp"
			
	def crear_combos_modelo_afp(self):
		self.modelo_afp= gtk.ListStore(str) 
		self.comboboxentryAfp.set_model(self.modelo_afp)
		cell=gtk.CellRendererText()
		self.comboboxentryAfp.pack_start(cell,True)
		self.comboboxentryAfp.add_attribute(cell,'text',0)
		return

	
	def llenar_combos_salud(self):
		self.modelo_salud.clear()
		
		sql	="""
			 SELECT nombre_salud
			 FROM salud
			 ORDER BY nombre_salud
			 """
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if not len(r)==0:
			for i in r:
				self.modelo_salud.append(i)	
		else:
			print "no existen isapres o Fonasa"
			
	def crear_combos_modelo_salud(self):
		self.modelo_salud= gtk.ListStore(str) 
		self.comboboxentrySalud.set_model(self.modelo_salud)
		cell=gtk.CellRendererText()
		self.comboboxentrySalud.pack_start(cell,True)
		self.comboboxentrySalud.add_attribute(cell,'text',0)
		return


	def on_toolbuttonActualizar_clicked(self, toolbuttonActualizar=None):
		print "actualizar"
	
	def on_toolbuttonAtras_clicked(self, toolbuttonAtras=None):
		self.padre.notebookMain.prev_page()
	
	def on_toolbuttonAdelante_clicked(self, toolbuttonAdelante=None):
		self.padre.notebookMain.next_page()
		page = self.padre.notebookMain.get_current_page()
		self.padre.finingresartrabajador.toolbuttonGuardar.set_sensitive(True)
		self.padre.finingresartrabajador.toolbuttonAtras.set_sensitive(True)

	def on_comboboxentryAfp_changed(self,combo=None):
		model_aux = self.comboboxentryAfp.get_model()
		active = self.comboboxentryAfp.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentryAfp.child.set_text(elemento)
		return
	
	def on_comboboxentrySalud_changed(self,combo=None):
		model_aux = self.comboboxentrySalud.get_model()
		active = self.comboboxentrySalud.get_active()
		if active < 0:
			return None
		elemento= model_aux[active][0]
		self.comboboxentrySalud.child.set_text(elemento)
		if (elemento=='FONASA'):
			self.frameAdicionalPactado.hide()
			self.radiobuttonPoseeNo.set_active(True)
			if (self.padre.ingresarseleccionar.activo==1):
				self.toolbuttonPrestamoSalud.set_sensitive(True)
		else:
			self.frameAdicionalPactado.show_all()
			self.toolbuttonPrestamoSalud.set_sensitive(False)
			
		return
	
	def on_toolbuttonPrestamoCaja_clicked(self, toolbuttonPrestamoCaja=None):
		self.prestamocaja=PrestamoCajaCompensacion(self.cursor,self.padre.ingresarseleccionar.entryRutTrabajador.get_text(),self.padre)
		self.prestamocaja.windowPrestamoCaja.show()
		
	def on_toolbuttonPrestamoEmpresa_clicked(self, toolbuttonPrestamoEmpresa=None):
		self.prestamoempresa=PrestamoEmpresa(self.cursor,self.padre.ingresarseleccionar.entryRutTrabajador.get_text())
		self.prestamoempresa.padre=self.padre
		self.prestamoempresa.window1.show()
		
	def on_toolbuttonPrestamoSalud_clicked(self, toolbuttonPrestamoSalud=None):
		self.prestamofonasa=PrestamoFonasa(self.cursor, self.padre.ingresarseleccionar.entryRutTrabajador.get_text())
		self.prestamofonasa.padre=self.padre
		self.prestamofonasa.windowPrestamoFonasa.show()
	
	def on_toolbuttonDescuento_clicked(self,toolbuttonDescuento=None):
		self.descuento_trabajador=DescuentoTrabajador(self.cursor,self.padre.ingresarseleccionar.entryRutTrabajador.get_text(),self.padre)
		self.descuento_trabajador.window1.show()
	
	
	def on_radiobuttonPoseeNo_toggled(self, radioboton=None):
		if self.radiobuttonPoseeNo.get_active():
			self.entryCantidadUF.set_sensitive(False)
			self.entryCantidadUF.set_text("")
		else:
			self.entryCantidadUF.set_sensitive(True)
			self.entryCantidadUF.set_text("")
	
	def on_radiobuttonCompaniaSeguroVidaNo_toggled(self, radiobutton=None):
		if self.radiobuttonCompaniaSeguroVidaNo.get_active():
			self.comboboxentrySeleccionarCompania.set_sensitive(False)
			self.comboboxentrySeleccionarCompania.child.set_sensitive(False)
			self.entryNumeroCuotaSeguro.set_sensitive(False)
			self.entryValorSeguro.set_sensitive(False)
			self.entryNumeroCuotaSeguro.set_text("")
			self.entryValorSeguro.set_text("")
			self.comboboxentrySeleccionarCompania.child.set_text("")

		else:
			self.comboboxentrySeleccionarCompania.set_sensitive(True)
			self.entryNumeroCuotaSeguro.set_sensitive(True)
			self.entryValorSeguro.set_sensitive(True)
			self.entryNumeroCuotaSeguro.set_text("")
			self.entryValorSeguro.set_text("")

	
	def on_radiobuttonCajaSeguroVidaNo_toggled(self, radiobutton=None):
		if self.radiobuttonCajaSeguroVidaNo.get_active():
			self.comboboxentrySeleccionarCaja.set_sensitive(False)
			self.comboboxentrySeleccionarCaja.child.set_sensitive(False)
			self.entryCajaNumeroCuota.set_sensitive(False)
			self.entryCajaValor.set_sensitive(False)
			self.entryCajaNumeroCuota.set_text("")
			self.entryCajaValor.set_text("")
			self.comboboxentrySeleccionarCaja.child.set_text("")
		else:
			self.comboboxentrySeleccionarCaja.set_sensitive(True)
			self.entryCajaNumeroCuota.set_sensitive(True)
			self.entryCajaValor.set_sensitive(True)
			self.entryCajaNumeroCuota.set_text("")
			self.entryCajaValor.set_text("")
	
	def on_radiobuttonSeguroCesantiaNo_toggled(self, radiobutton=None):
		if self.radiobuttonSeguroCesantiaNo.get_active():
			self.entryPorcientoSeguroDesempleo.set_sensitive(False)
			self.entryPorcientoSeguroDesempleo.set_text("")
		else:
			self.entryPorcientoSeguroDesempleo.set_sensitive(True)
			self.entryPorcientoSeguroDesempleo.set_text("")
	
	def on_radiobuttonLeasingNo_toggled(self, radiobutton=None):
		if self.radiobuttonLeasingNo.get_active():
			self.entryRutCodigoInterno.set_sensitive(False)
			self.entryNumeroCuenta.set_sensitive(False)
			self.entryNumeroCuota.set_sensitive(False)
			self.entryAporteUFPorcentajeRemuneracion.set_sensitive(False)
			self.entryRutCodigoInterno.set_text("")
			self.entryNumeroCuenta.set_text("")
			self.entryNumeroCuota.set_text("")
			self.entryAporteUFPorcentajeRemuneracion.set_text("")
		else:
			self.entryRutCodigoInterno.set_sensitive(True)
			self.entryNumeroCuenta.set_sensitive(True)
			self.entryNumeroCuota.set_sensitive(True)
			self.entryAporteUFPorcentajeRemuneracion.set_sensitive(True)
			self.entryRutCodigoInterno.set_text("")
			self.entryNumeroCuenta.set_text("")
			self.entryNumeroCuota.set_text("")
			self.entryAporteUFPorcentajeRemuneracion.set_text("")
		
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
