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
from gtk import TRUE, FALSE
import pygtk
pygtk.require('2.0')
import gtk


class MovimientoPersonal(GladeConnect):
	def __init__(self, cursor):
		GladeConnect.__init__(self, "glade/t_pl_movimientopersonal.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.radiobuttonSi.set_active(True)
		self.entryNombreTrabajador.set_sensitive(False)
		self.comboboxentryMovimientoPersonal.set_sensitive(False)
		self.pactado_adicional=None

	def on_radiobuttonNo_toggled(self, radiobutton=None):
		if self.radiobuttonNo.get_active():
			self.on_comboboxentryMovimientoPersonal_changed()

	def on_comboboxentryMovimientoPersonal_changed(self, argumento=None):
		self.padre.notebookMain.next_page()
		self.padre.t_pl_antecedentesliquidacion.notebook1.set_current_page(0)
		self.padre.t_pl_antecedentesliquidacion.notebook2.set_current_page(0)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonAtras.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonGenerarLiquidacion.set_sensitive(True)

		#borrando informacion de cajas
		self.padre.t_pl_antecedentesliquidacion.entryNombreAfp.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryTipoAfiliado.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryFactorHorasExtras.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryTramoCarga.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCargasRetroactivas.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryValorTotal.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCotizacionObligatoria.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryAhorroVoluntario.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entrySalud.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryDescuentoSalud.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryFactorHorasExtras.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryColacion.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryMovilizacion.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCargas.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCargasRetroactivas.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryValorTotal.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCompaniaSeguroVidaPosee.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCompania.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCompania.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryValorCompania.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCompania.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryValorCompania.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryOptaSeguroCesantia.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryPorcientroSeguroDesempleo.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryRutCodigoInterno.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuenta.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuota.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryRutCodigoInterno.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuenta.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuota.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCajaSeguroVidaPosee.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryCajaCompensacion.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCaja.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryValorCaja.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCaja.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryValorCaja.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryHorasExtras.set_text("0")
		self.padre.t_pl_antecedentesliquidacion.entryViaticos.set_text("0")
		self.padre.t_pl_antecedentesliquidacion.entryAporteDinero.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryInicioVacaciones.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryFinVacaciones.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryInicioLicencia.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryFinLicencia.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryInicioPermiso.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryFinPermiso.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryDiasVacaciones.set_text("0")
		self.padre.t_pl_antecedentesliquidacion.entryDiasLicencia.set_text("0")
		self.padre.t_pl_antecedentesliquidacion.entryDiasPermiso.set_text("0")
		self.padre.t_pl_antecedentesliquidacion.entryAnticipos.set_text("0")

		#poniendo botones en falso
		self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioLicencia.set_sensitive(False)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonFinLicencia.set_sensitive(False)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioVacaciones.set_sensitive(False)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonFinVacaciones.set_sensitive(False)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioPermiso.set_sensitive(False)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonFinPermiso.set_sensitive(False)
		#llenando cajas con informacion por default

		sql="""SELECT t.tramo_carga_trabajador, a.codigo_antecedente_liquidacion,
		    a.nombre_compania_seguro,a.nombre_salud,
		    a.rut_trabajador,a.nombre_caja_compensacion,
		    a.nombre_afp,a.sueldo_base,
		    a.factor_hora_extras,a.colacion,
		    a.movilizacion,a.numero_cargas,
		    a.cargas_retroactivas,a.valor_total,
		    a.afp_tipo_afiliado,
		    a.ahorro_voluntario,a.seguro_cesantia,
		    a.seguro_cesantia_porcen,
		    a.adicional_pactado,a.monto_adicional_pactado_uf,
		    a.posee_seguro_vida_c_s,a.s_v_c_numerocuota,
		    a.s_v_c_s_valor,a.leasing_rut_codigo,
		    a.leasing_numero_cuenta,a.leasing_numero_cuota,
		    a.leasing_aporteuf_remuneracion,a.posee_s_v_c_c,
		    a.s_v_c_c_numero_cuota,a.s_v_c_c_valor,
		    t.cargo_trabajador
		    FROM trabajador t, antecedente_liquidacion a
		    WHERE a.rut_trabajador=t.rut_trabajador 
		    and t.rut_trabajador='%s'
		    """%(self.padre.listatrabajadores.rut_trabajador)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		self.pactado_adicional=r[0][19]
		self.padre.t_pl_antecedentesliquidacion.entryNombreAfp.set_text(r[0][6])
		self.padre.t_pl_antecedentesliquidacion.entryTipoAfiliado.set_text(r[0][14])
		self.padre.t_pl_antecedentesliquidacion.entrySueldoBase.set_text(str(r[0][7]))
		self.padre.t_pl_antecedentesliquidacion.entryFactorHorasExtras.set_text(str(r[0][8]))
		self.padre.t_pl_antecedentesliquidacion.entryColacion.set_text(str(r[0][9]))
		self.padre.t_pl_antecedentesliquidacion.entryMovilizacion.set_text(str(r[0][10]))
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCargas.set_text(str(r[0][11]))
		self.padre.t_pl_antecedentesliquidacion.entryTramoCarga.set_text(str(r[0][0]))
		self.padre.t_pl_antecedentesliquidacion.entryCargasRetroactivas.set_text(str(r[0][12]))
		self.padre.t_pl_antecedentesliquidacion.entryValorTotal.set_text(str(r[0][13]))
		self.padre.t_pl_antecedentesliquidacion.entryAhorroVoluntario.set_text(str(r[0][15]))
		self.padre.t_pl_antecedentesliquidacion.entrySalud.set_text(r[0][3])
		#habilitando cajas que corresponden
		self.padre.t_pl_antecedentesliquidacion.entrySueldoBase.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryFactorHorasExtras.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryColacion.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryMovilizacion.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryNumeroCargas.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryCargasRetroactivas.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryValorTotal.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryCotizacionObligatoria.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryAhorroVoluntario.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryDescuentoSalud.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.entryAnticipos.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.toolbuttonAnticipos.set_sensitive(True)
		
		
		if r[0][20]=='SI':
			self.padre.t_pl_antecedentesliquidacion.entryCompaniaSeguroVidaPosee.set_text("SI")
			self.padre.t_pl_antecedentesliquidacion.entryCompania.set_text(r[0][2])
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCompania.set_text(str(r[0][21]))
			self.padre.t_pl_antecedentesliquidacion.entryValorCompania.set_text(str(r[0][22]))
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCompania.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryValorCompania.set_sensitive(True)
		else:
			self.padre.t_pl_antecedentesliquidacion.entryCompaniaSeguroVidaPosee.set_text("NO")
		if r[0][16]=='SI':
			self.padre.t_pl_antecedentesliquidacion.entryOptaSeguroCesantia.set_text("SI")
			self.padre.t_pl_antecedentesliquidacion.entryPorcientroSeguroDesempleo.set_text(str(r[0][17]))
		else:
			self.padre.t_pl_antecedentesliquidacion.entryOptaSeguroCesantia.set_text("NO")
		
		
		if not (r[0][23]==None or r[0][23]==" "):
			self.padre.t_pl_antecedentesliquidacion.entryRutCodigoInterno.set_text(r[0][23])
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuenta.set_text(str(r[0][24]))
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuota.set_text(str(r[0][25]))
			self.padre.t_pl_antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_text(str(r[0][26]))
			self.padre.t_pl_antecedentesliquidacion.entryRutCodigoInterno.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuenta.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuota.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryAporteDinero.set_sensitive(True)
		else:
			self.padre.t_pl_antecedentesliquidacion.entryRutCodigoInterno.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuenta.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuota.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryAporteDinero.set_sensitive(False)
		
		if r[0][27]=='SI':
			self.padre.t_pl_antecedentesliquidacion.entryCajaSeguroVidaPosee.set_text("SI")
			self.padre.t_pl_antecedentesliquidacion.entryCajaCompensacion.set_text(r[0][5])
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCaja.set_text(str(r[0][28]))
			self.padre.t_pl_antecedentesliquidacion.entryValorCaja.set_text(str(r[0][29]))
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCaja.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryValorCaja.set_sensitive(True)
		else:
			self.padre.t_pl_antecedentesliquidacion.entryCajaSeguroVidaPosee.set_text("NO")
		
		self.padre.t_pl_antecedentesliquidacion.entryHorasExtras.set_sensitive(True)
		self.padre.t_pl_antecedentesliquidacion.tipo_trabajador=r[0][30]
		if (self.padre.t_pl_antecedentesliquidacion.tipo_trabajador=='CONDUCTOR DE BUS' or self.padre.t_pl_antecedentesliquidacion.tipo_trabajador=='AUXILIAR DE BUS'):		
			self.padre.t_pl_antecedentesliquidacion.toolbuttonVueltas.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryBonoViajes.set_text("")
			self.padre.t_pl_antecedentesliquidacion.entryBonoViajes.set_text("0")
		else:
			self.padre.t_pl_antecedentesliquidacion.toolbuttonVueltas.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryBonoViajes.set_text("")
			self.padre.t_pl_antecedentesliquidacion.entryBonoViajes.set_text("0")
		
		if self.padre.t_pl_antecedentesliquidacion.tipo_trabajador=='ADMINISTRATIVO':
			self.padre.t_pl_antecedentesliquidacion.entryViaticos.set_sensitive(False)
		else:
			self.padre.t_pl_antecedentesliquidacion.entryViaticos.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryViaticos.set_text("0")
		
		self.padre.t_pl_antecedentesliquidacion.entryHorasExtras.set_text("0")
				
		if self.padre.t_pl_antecedentesliquidacion.entryCompaniaSeguroVidaPosee.get_text()=="NO":
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCompania.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryValorCompania.set_sensitive(False)
		else:
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCompania.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryValorCompania.set_sensitive(True)
		
		if self.padre.t_pl_antecedentesliquidacion.entryCajaSeguroVidaPosee.get_text()=="NO":
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCaja.set_sensitive(False)
			self.padre.t_pl_antecedentesliquidacion.entryValorCaja.set_sensitive(False)
		else:
			self.padre.t_pl_antecedentesliquidacion.entryNumeroCuotaCaja.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.entryValorCaja.set_sensitive(True)
		
		if self.comboboxentryMovimientoPersonal.child.get_text()=="LICENCIA MEDICA":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioLicencia.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="PERMISO S.G.S.":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioPermiso.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="FERIADO LEGAL":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioVacaciones.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="LICENCIA MEDICA, PERMISO S.G.S., FERIADO LEGAL":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioLicencia.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioVacaciones.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioPermiso.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="LICENCIA MEDICA, PERMISO S.G.S.":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioLicencia.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioPermiso.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="LICENCIA MEDICA, FERIADO LEGAL":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioLicencia.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioVacaciones.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="PERMISO S.G.S., FERIADO LEGAL":
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioPermiso.set_sensitive(True)
			self.padre.t_pl_antecedentesliquidacion.toolbuttonInicioVacaciones.set_sensitive(True)
		elif self.comboboxentryMovimientoPersonal.child.get_text()=="FINIQUITO":
			print "FALTA DEFINIR FINIQUITO" 
		
		self.padre.t_pl_antecedentesliquidacion.datos_liquidacion_sueldo={}
		self.padre.t_pl_antecedentesliquidacion.entryDiasTrabajados.set_text("")
		self.padre.t_pl_antecedentesliquidacion.entryDiasTrabajados.set_text("30")
		self.padre.t_pl_antecedentesliquidacion.llenar_prestamo_caja()
		self.padre.t_pl_antecedentesliquidacion.llenar_prestamo_empleador()
		self.padre.t_pl_antecedentesliquidacion.llenar_prestamo_fonasa()
		self.padre.t_pl_antecedentesliquidacion.llenar_otros_descuentos()
		self.padre.listatrabajadores.movimientopersonal.dialog1.destroy()
		
		#print self.padre.t_pl_antecedentesliquidacion.diccionario_caja
		#print self.padre.t_pl_antecedentesliquidacion.diccionario_empresa
		#print self.padre.t_pl_antecedentesliquidacion.diccionario_otros_descuentos
		
		
		sql="""SELECT procesado
		FROM trabaja
		WHERE rut_trabajador='%s'
		AND rut_empresa='%s'
		"""%(self.padre.listatrabajadores.rut_trabajador,
		self.padre.rut_empresa_actual)
		self.cursor.execute(sql)
		r=self.cursor.fetchall()
		if r[0][0]==1:
			sql	="""SELECT codigo_proceso
					FROM proceso_remuneracion
					WHERE rut_empresa='%s' 
					AND estado_proceso='ABIERTO'  
				"""%(self.padre.rut_empresa_actual)
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			sql="""SELECT historico_bono_viajes, 
			historico_anticipos, historico_gtk_model
			FROM historico_liquidacion
			WHERE codigo_proceso='%s'
			AND rut_trabajador='%s'
			"""%(r[0][0],
			self.padre.listatrabajadores.rut_trabajador)
			self.cursor.execute(sql)
			r=self.cursor.fetchall()
			self.padre.t_pl_antecedentesliquidacion.entryBonoViajes.set_text(str(r[0][0]))
			self.padre.t_pl_antecedentesliquidacion.entryAnticipos.set_text(str(r[0][1]))
			if not r[0][2]=='[]':
				self.padre.t_pl_antecedentesliquidacion.modelo_vueltas=gtk.ListStore(str,str,str,str)
				for i in eval(r[0][2]):
					self.padre.t_pl_antecedentesliquidacion.modelo_vueltas.append(i)
			else:
				self.padre.t_pl_antecedentesliquidacion.modelo_vueltas=None
		self.padre.notebookMain.next_page()
		self.padre.vbox1.set_sensitive(True)
		
	def on_dialog1_delete_event(self, Widget=None, Event=None):
		self.padre.vbox1.set_sensitive(True)
		return False
