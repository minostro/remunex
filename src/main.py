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
import gtk.glade
from gtk import *

#importar todas las clases necesarias
from afp import *
from salud import *
from cajacompensacion import *
from mutualseguridad import *
from empleador import *
from trabajador import *
from conexionempresa import *
from finingresartrabajador import *
from acercade import *
from procesarliquidacion import *
from calendario import *
from t_pl_listatrabajadores import *
from t_pl_movimientopersonal import *
from pe_montosfactorestopes import *
from pe_tramoscargasfamiliares import *
from conexionbd import *
from t_pl_antecedentesliquidacion import *
from companiaseguro import *
from bono_viajes import *
from nuevo_proceso import *
from descuento import *
from dialogo_error import DialogoError
from types import StringType
from numeros_a_letras import *


class RemunexMain(GladeConnect):
	def __init__(self):
		GladeConnect.__init__(self, "glade/main.glade")
		self.wins={}
		self.fecha_proceso=None
		self.fecha_actual=None
		self.rut_empresa_actual=None
		self.razon_social_empresa=None
		self.anio=None
		self.mes=None
		self.dia=None
		self.empleador=None
		self.l=None
		self.windowMain.maximize()
		self.notebookMain.set_scrollable(1)
		self.ventana_activa = None
		#deja opciones de menu deshabilitadas
		self.trabaja2.set_sensitive(False)
		self.desconectar.set_sensitive(False)
		self.imprimir2.set_sensitive(False)
		self.especificos.set_sensitive(False)
		self.windowMain.set_sensitive(False)
		#base de datos
		self.cnx =None
		self.cursor=None 
		#establece conexion con base de datos
		self.conectarbd=Conectar_bd()
		self.conectarbd.dialog1.show_all()
		self.conectarbd.padre=self
		#crea diccionario para eliminar presentacion inicial
		self.pi={}
		self.pi["presentacion"]=("presentacion")
		
	def _nueva_pagina(self, widget, label):
		if not self.wins.has_key(label):
			v = gtk.VBox()
			l = gtk.Label('')
			l.set_text_with_mnemonic(label)
			self.notebookMain.append_page(v, l)
			v.show()
			widget.reparent(v)
			self.wins[label] = (v, widget, len(self.wins))
		
		else:
			self.notebookMain.show_all()
			self.notebookMain.set_current_page(self.wins[label][2])
			a = self.notebookMain.get_current_page()
		#deja activa la primera lengueta del notebook
		self.notebookMain.set_current_page(0)	
		return
	
	def on_parametros_generales_activate(self,source=None,event=None):
		if self.l==1:
			self.activar_remuneracion()
			
		if self.pi.has_key("presentacion"):
			self.notebookMain.remove_page(0)
			self.notebookMain.set_show_tabs(True)
			self.pi={}
		
		if not self.wins.has_key("Gestion de Afp"):
			self.parametros_generales.set_sensitive(False)
			self.parametros_especificos.set_sensitive(True)
			self.activar_especificos()
			if len(self.wins):
				aux=self.wins
				for i in aux:
					self.notebookMain.remove_page(0)
				self.wins={}
			self.afp = Afp(self.cursor)
			self._nueva_pagina(self.afp.vboxAfp,"Gestion de Afp")
			self.afp.padre = self
		
			self.salud = Salud(self.cursor)
			self._nueva_pagina(self.salud.vboxSalud,"Gestion de Salud")
			self.salud.padre = self
		
			self.cajacompensacion = CajaCompensacion(self.cursor)
			self._nueva_pagina(self.cajacompensacion.vboxCajaCompensacion,"Gestion Caja de Compensacion")
			self.cajacompensacion.padre = self
		
			self.mutualseguridad = MutualSeguridad(self.cursor)
			self._nueva_pagina(self.mutualseguridad.vboxMutualSeguridad,"Gestion Mutual de Seguridad")
			self.mutualseguridad.padre = self

			self.companiaseguro = CompaniaSeguro(self.cursor)
			self._nueva_pagina(self.companiaseguro.vboxCompaniaSeguro,"Gestion Compania de Seguros")
			self.companiaseguro.padre = self
			
			self.empleador = Empleador(self.cursor)
			self._nueva_pagina(self.empleador.vboxEmpleador,"Gestion de Empleador")
			self.empleador.padre = self
			return

		return
	
	def on_especificos1_activate(self,source=None,event=None):
		if self.l==1:
			self.activar_remuneracion()
			
		if self.pi.has_key("presentacion"):
			self.notebookMain.remove_page(0)
			self.notebookMain.set_show_tabs(True)
			self.pi={}
			
		if not self.wins.has_key("Montos - Factores - Topes"):
			self.parametros_especificos.set_sensitive(False)
			self.parametros_generales.set_sensitive(True)
			self.activar_especificos()
			if len(self.wins):
				aux=self.wins
				for i in aux:
					self.notebookMain.remove_page(0)
				self.wins={}
		
			self.montosfactorestopes=MontosFactoresTopes(self.cursor)
			self._nueva_pagina(self.montosfactorestopes.vboxMontosFactoresTopes,"Montos - Factores - Topes")
			self.montosfactorestopes.padre=self
				
			self.tramoscargasfamiliares=TramosCargasFamiliares(self.cursor)
			self._nueva_pagina(self.tramoscargasfamiliares.vboxTramosCargasFamiliares,"Gestion Tramos Cargas Familiares")
			self.tramoscargasfamiliares.padre=self
			
			self.bono_viajes=BonoViajes(self.cursor,self.rut_empresa_actual)
			self._nueva_pagina(self.bono_viajes.vboxBonoViajes,"Gestion de Vueltas")
			self.bono_viajes.padre = self
			
		return


	def on_gestion_de_trabajador1_activate(self,source=None,event=None):
		if self.l==1:
			self.activar_remuneracion()
		self.parametros_especificos.set_sensitive(True)
		self.gestion_de_trabajador1.set_sensitive(False)
		self.gestion_de_descuentos1.set_sensitive(True)
		self.parametros_generales.set_sensitive(True)
	
		if not self.wins.has_key("Ingresar - Seleccionar"):
			if len(self.wins):
				aux=self.wins
				for i in aux:
					self.notebookMain.remove_page(0)
				self.wins={}		

			self.ingresarseleccionar = IngresarSeleccionar(self.cursor, self.rut_empresa_actual)
			self._nueva_pagina(self.ingresarseleccionar.vboxIngresarSeleccionar,"Ingresar - Seleccionar")
			self.ingresarseleccionar.padre = self
		
			self.antecedentespersonales = AntecedentesPersonales(self.cursor)
			self._nueva_pagina(self.antecedentespersonales.vboxAntecedentesPersonales,"Antecedentes Personales")
			self.antecedentespersonales.padre = self
			self.ingresarseleccionar.hermano=self.antecedentespersonales
					
			self.antecedentesliquidacion = AntecedentesLiquidacion(self.cursor,self.fecha_proceso)
			self._nueva_pagina(self.antecedentesliquidacion.vboxAntecedentesLiquidacion, "Antecedentes Liquidacion")
			self.antecedentesliquidacion.padre = self
			self.antecedentespersonales.hermano=self.antecedentesliquidacion
			
			self.finingresartrabajador = FinIngresarTrabajador(self.cursor)
			self.finingresartrabajador.padre = self		
		return
		
	def on_conectar_activate(self,source=None, event=None):
		a= ConexionEmpresa(self.cursor)
		a.padre=self
	
	def on_desconectar_activate(self, source=None, event=None):
		if len(self.wins):
				aux=self.wins
				for i in aux:
					self.notebookMain.remove_page(0)
				self.wins={}	
		self.desconectar.set_sensitive(False)
		self.conectar.set_sensitive(True)
		
		self.trabaja2.set_sensitive(False)
		self.nuevo_proceso1.set_sensitive(True)
		self.cerrar_proceso1.set_sensitive(True)		
		self.liquidacion_de_sueldo1.set_sensitive(True)
		self.libro_remuneraciones.set_sensitive(True)
		self.especificos.set_sensitive(False)
		self.parametros_generales.set_sensitive(True)
		self.activar_especificos()
		self.imprimir2.set_sensitive(False)
		
		
	def on_liquidacion_de_sueldo1_activate(self,source=None, event=None):
		self.l=1
		self.activar_especificos()
		a=ProcesarLiquidacion()
		a.padre=self
	
	#def on_gestion_de_vueltas1_activate(self,source=None, event=None):
	#	if self.l==1:
	#		self.activar_remuneracion()
	#	if self.pi.has_key("presentacion"):
	#		self.notebookMain.remove_page(0)
	#		self.notebookMain.set_show_tabs(True)
	#		self.pi={}
	#	self.gestion_de_vueltas1.set_sensitive(False)
	#	self.parametros_especificos.set_sensitive(True)
	#	self.gestion_de_trabajador1.set_sensitive(True)
	#	self.gestion_de_descuentos1.set_sensitive(True)
	#	self.parametros_generales.set_sensitive(True)
	#	if not self.wins.has_key("Gestion de Vueltas"):
	#		if len(self.wins):
	#			aux=self.wins
	#			for i in aux:
	#				self.notebookMain.remove_page(0)
	#			self.wins={}
			
	def construir_ventanas_liquidacion_sueldo_uno_a_uno(self):
		
		self.listatrabajadores = ListaTrabajadores(self.cursor, self.rut_empresa_actual)
		self._nueva_pagina(self.listatrabajadores.vboxListaTrabajadores,"Seleccionar Trabajador")
		self.listatrabajadores.padre = self
				
		self.t_pl_antecedentesliquidacion= t_pl_AntecedentesLiquidacion(self.cursor)
		self._nueva_pagina(self.t_pl_antecedentesliquidacion.vboxt_pl_AntecedentesLiquidacion,"Antecedentes Liquidacion")
		self.t_pl_antecedentesliquidacion.padre = self
		return
				
	
	def on_notebookMain_switch_page	(self, widget=None, puntero=None, NumeroPagina=None):
		if NumeroPagina==1:
			if self.wins.has_key("Gestion de Salud"):
				self.salud.lista_datos()
				return
			
		if NumeroPagina==2:
			if self.wins.has_key("Gestion Caja de Compensacion"):
				self.cajacompensacion.lista_datos()
				return

		if NumeroPagina==3:
			if self.wins.has_key("Gestion Mutual de Seguridad"):
				self.mutualseguridad.lista_datos()
				return

		if NumeroPagina==4 and self.wins.has_key("Gestion Compania de Seguros"):
			self.companiaseguro.lista_datos()
			return

		if NumeroPagina==5 and self.wins.has_key("Gestion de Empleador"):
			self.empleador.lista_datos()
			return
	
	
	def on_acerca_de1_activate(self, acercade=None):
		a = AcercaDe()
		self._nueva_pagina(a.dialog-vbox1,"Acerca De")
		a.padre = self

	def on_windowMain_delete_event(self, Widget=None, Event=None):
		gtk.main_quit()
	
	def on_salir1_activate(self, salir=None):
		gtk.main_quit()
		
	def on_nuevo_proceso1_activate(self, nuevo_proceso=None):
		sql	="""SELECT codigo_proceso
		FROM proceso_remuneracion
		WHERE rut_empresa='%s'
		"""%(self.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			self.nuevo_proceso=NuevoProceso(self.cursor,0,self)
			self.nuevo_proceso.dialog1.show()
			self.nuevo_proceso.padre=self
		else:
			self.nuevo_proceso=NuevoProceso(self.cursor,1,self)
			self.nuevo_proceso.dialog1.show()
			self.nuevo_proceso.padre=self
	
	def on_gestion_de_descuentos1_activate(self, gestion=None):
		if self.l==1:
			self.activar_remuneracion()
		self.gestion_de_descuentos1.set_sensitive(False)
		self.parametros_especificos.set_sensitive(True)
		self.gestion_de_trabajador1.set_sensitive(True)
		self.parametros_generales.set_sensitive(True)
		if not self.wins.has_key("Gestion Descuentos"):
			if len(self.wins):
				aux=self.wins
				for i in aux:
					self.notebookMain.remove_page(0)
				self.wins={}
			descuento=Descuento(self.cursor,self)
			self._nueva_pagina(descuento.vboxDescuentos,"Gestion Descuentos")
	
	def activar_especificos(self):
		self.gestion_de_trabajador1.set_sensitive(True)
		self.gestion_de_descuentos1.set_sensitive(True)
		return
	
	def activar_remuneracion(self):
		self.cerrar_proceso1.set_sensitive(True)
		self.liquidacion_de_sueldo1.set_sensitive(True)
		self.libro_remuneraciones.set_sensitive(True)
		return
	
	def on_cerrar_proceso1_activate(self, cerrar=None):
		sql="""SELECT *
		FROM trabaja
		WHERE rut_empresa='%s'
		AND procesado=0
		"""%(self.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if len(r)==0:
			sql	="""SELECT codigo_proceso
			FROM proceso_remuneracion
			WHERE rut_empresa='%s'
			AND estado_proceso='ABIERTO'  
			"""%(self.rut_empresa_actual)
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			codigo_proceso=r[0][0]
			
			sql="""SELECT t.nombres_trabajador,
			t.apellido_paterno_trabajador,
			t.apellido_materno_trabajador,
			t.rut_trabajador,
			h.historico_sueldo_base,
			h.historico_bono_viajes,
			h.historico_total_remuneracion_im,
			h.historico_numero_cargas,
			h.historico_valor_cargas,
			h.historico_movilizacion,
			h.historico_viaticos,
			h.historico_total_haber,
			h.historico_cotizacion_previsiona,
			h.historico_descuento_salud,
			h.historico_total_prestamos,
			h.historico_total_otros,
			h.historico_total_descuentos,
			h.historico_alcance_liquido,
			h.historico_anticipos,
			h.historico_saldo_liquido
			FROM trabajador t, historico_liquidacion h
			WHERE h.codigo_proceso='%s'
			AND t.rut_trabajador=h.rut_trabajador
			"""%(codigo_proceso)
			self.cursor.execute(sql)
			listado_trabajadores=self.cursor.fetchall()
			
			#CREAR LIBRO DE REMUNERACIONES PDF :D|D:
			
			total_sueldo_base=0
			total_bono_viajes=0
			total_remuneracion_imponible=0
			total_numero_cargas=0
			total_valor_cargas=0
			total_movilizacion=0
			total_viaticos=0
			total_haber=0
			total_cotizacion_previsional=0
			total_descuento_salud=0
			total_prestamos=0
			total_otros=0
			total_descuento=0
			total_alcance_liquido=0
			total_anticipos=0
			total_saldo_liquido=0
			
			for i in range(len(listado_trabajadores)):
				total_sueldo_base=total_sueldo_base+int(listado_trabajadores[i][4])
				total_bono_viajes=total_bono_viajes+int(listado_trabajadores[i][5])
				total_remuneracion_imponible=total_remuneracion_imponible+int(listado_trabajadores[i][6])
				total_numero_cargas=total_numero_cargas+int(listado_trabajadores[i][7])
				total_valor_cargas=total_valor_cargas+int(listado_trabajadores[i][8])
				total_movilizacion=total_movilizacion+int(listado_trabajadores[i][9])
				total_viaticos=total_viaticos+int(listado_trabajadores[i][10])
				total_haber=total_haber+int(listado_trabajadores[i][11])
				total_cotizacion_previsional=total_cotizacion_previsional+int(listado_trabajadores[i][12])
				total_descuento_salud=total_descuento_salud+int(listado_trabajadores[i][13])
				total_prestamos=total_prestamos+int(listado_trabajadores[i][14])
				total_otros=total_otros+int(listado_trabajadores[i][15])
				total_descuento=total_descuento+int(listado_trabajadores[i][16])
				total_alcance_liquido=total_alcance_liquido+int(listado_trabajadores[i][17])
				total_anticipos=total_anticipos+int(listado_trabajadores[i][18])
				total_saldo_liquido=total_saldo_liquido+int(listado_trabajadores[i][19])
			
			print total_sueldo_base
			print total_bono_viajes
			print total_remuneracion_imponible
			print total_numero_cargas
			print total_valor_cargas
			print total_movilizacion
			print total_viaticos
			print total_haber
			print total_cotizacion_previsional
			print total_descuento_salud
			print total_prestamos
			print total_otros
			print total_descuento
			print total_alcance_liquido
			print total_anticipos
			print total_saldo_liquido
			
		else:
			texto="Aun no puede cerrar proceso, le falta por procesar a"
			if len(r)>1:
				texto=texto+" %s trabajadores"%(numerals(len(r)))
			else:
				texto=texto+" un trabajador"
			string = StringType(texto)
			string = unicode(string,"iso8859-15")
			string = string.encode("utf-8")			
			dialogo_error=DialogoError(string)
			dialogo_error.dialog1.show_all()
			dialogo_error.padre=self
			self.vbox1.set_sensitive(False)
		
if __name__ == "__main__":
	RemunexMain()
	gtk.main()
