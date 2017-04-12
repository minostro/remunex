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
import sys
import gobject
import gtk
from gtk import TRUE, FALSE
from dialogo_error import DialogoError
from types import StringType


class FinIngresarTrabajador(GladeConnect):
	"agregar comentario"
	
	def __init__(self,cursor):
		GladeConnect.__init__(self, "glade/finingresartrabajador.glade")
		self.cursor=cursor
		self.ventana_activa = None
		self.padre = None
		self.hermano = None
		self.toolbuttonAtras.set_sensitive(False)
		self.toolbuttonGuardar.set_sensitive(False)
		
	
	
	def on_toolbuttonGuardar_clicked(self, toolbuttonGuardar=None):
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
						 INSERT INTO direccion
						 (nombre_comuna,nombre_calle_direccion,
						  numero_direccion,block_direccion,
						  departamento_direccion
						 )
						 VALUES ('%s','%s','%s','%s','%s')
						 """%(
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text(),
						 self.padre.antecedentespersonales.entryBlock.get_text().upper(),
						 self.padre.antecedentespersonales.entryDepartamento.get_text()
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
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text()
						 )
					self.cursor.execute(sql)
			else:
				if self.padre.antecedentespersonales.radiobuttonDepartamentoSi.get_active():
					sql ="""
						 INSERT INTO direccion
						 (nombre_comuna,nombre_calle_direccion,
						  numero_direccion,block_direccion,
						  departamento_direccion
						 )
						 VALUES ('%s','%s','%s','%s','%s')
						 """%(
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text(),
						 self.padre.antecedentespersonales.entryBlock.get_text().upper(),
						 self.padre.antecedentespersonales.entryDepartamento.get_text()
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
						 self.padre.antecedentespersonales.comboboxentryComuna.child.get_text().upper(),
						 self.padre.antecedentespersonales.entryCalle.get_text().upper(),
						 self.padre.antecedentespersonales.entryNumero.get_text()
						 )
					self.cursor.execute(sql)
				
			trabajador=[]
			trabajador.append(self.padre.ingresarseleccionar.entryRutTrabajador.get_text())
						
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
				
			trabajador.append(str(r[0][0]))
			trabajador.append(self.padre.ingresarseleccionar.entryApellidoPaterno.get_text().upper())
			trabajador.append(self.padre.ingresarseleccionar.entryApellidoMaterno.get_text().upper())
			trabajador.append(self.padre.ingresarseleccionar.entryNombres.get_text().upper())
			trabajador.append(self.padre.ingresarseleccionar.entryFechaNacimiento.get_text())	
			trabajador.append(self.padre.ingresarseleccionar.comboboxentrySexo.child.get_text().upper())
			trabajador.append(self.padre.ingresarseleccionar.comboboxentryNacionalidad.child.get_text().upper())
			trabajador.append(self.padre.antecedentespersonales.comboboxentryCargo.child.get_text().upper())
			trabajador.append(self.padre.antecedentespersonales.entryFechaIngreso.get_text())	
			auxiliar=self.padre.antecedentesliquidacion.comboboxentryTramoCargas.child.get_text()
			trabajador.append(auxiliar[0])
			trabajador.append(self.padre.antecedentespersonales.comboboxentryTipoContrato.child.get_text())
			
			sql ="""
				 INSERT INTO trabajador
				 VALUES("""+ ",".join(["'%s'" %(n1) for n1 in trabajador])+")"
			self.cursor.execute(sql)

			sql	="""
				 INSERT INTO trabaja
				 VALUES ('%s','%s')
				 """%(
				 self.padre.ingresarseleccionar.entryRutTrabajador.get_text(),
				 self.padre.rut_empresa_actual.upper(),
				 )
			self.cursor.execute(sql)
			#antecedente liquidacion
			antecedente_liquidacion={}
			antecedente_liquidacion["rut_empresa"]=(self.padre.rut_empresa_actual)
			if not self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaNo.get_active():
				antecedente_liquidacion["nombre_compania_seguro"]=(self.padre.antecedentesliquidacion.comboboxentrySeleccionarCompania.child.get_text().upper())
				
			antecedente_liquidacion["nombre_salud"]=(self.padre.antecedentesliquidacion.comboboxentrySalud.child.get_text().upper())
			antecedente_liquidacion["rut_trabajador"]=(self.padre.ingresarseleccionar.entryRutTrabajador.get_text())
			
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
						
			if not self.padre.antecedentesliquidacion.radiobuttonPoseeNo.get_active():
				antecedente_liquidacion["adicional_pactado"]=("SI")
				antecedente_liquidacion["monto_adicional_pactado_uf"]=(self.padre.antecedentesliquidacion.entryMontoAdicionalPactado.get_text())
			else:
				antecedente_liquidacion["adicional_pactado"]=("NO")
				antecedente_liquidacion["monto_adicional_pactado_uf"]=('0')
			
			
			if self.padre.antecedentesliquidacion.radiobuttonCompaniaSeguroVidaNo.get_active():
				antecedente_liquidacion["posee_seguro_vida_c_s"]=("NO")
			else:
				antecedente_liquidacion["posee_seguro_vida_c_s"]=("SI")
				antecedente_liquidacion["s_v_c_numerocuota"]=(self.padre.antecedentesliquidacion.entryNumeroCuotaSeguro.get_text())
				antecedente_liquidacion["s_v_c_s_valor"]=(self.padre.antecedentesliquidacion.entryValorSeguro.get_text())
			
			if self.padre.antecedentesliquidacion.radiobuttonLeasingSi.get_active():
				antecedente_liquidacion["leasing_rut_codigo"]=(self.padre.antecedentesliquidacion.entryRutCodigoInterno.get_text())
				antecedente_liquidacion["leasing_numero_cuenta"]=(self.padre.antecedentesliquidacion.entryNumeroCuenta.get_text())
				antecedente_liquidacion["leasing_numero_cuota"]=(self.padre.antecedentesliquidacion.entryNumeroCuota.get_text())
				antecedente_liquidacion["leasing_aporteuf_remuneracion"]=(self.padre.antecedentesliquidacion.entryAporteUFPorcentajeRemuneracion.get_text())
			
			if self.padre.antecedentesliquidacion.radiobuttonCajaSeguroVidaNo.get_active():
				antecedente_liquidacion["posee_s_v_c_c"]=("NO")
			else:
				antecedente_liquidacion["posee_s_v_c_c"]=("SI")
				antecedente_liquidacion["s_v_c_c_numero_cuota"]=(self.padre.antecedentesliquidacion.entryCajaNumeroCuota.get_text())
				antecedente_liquidacion["s_v_c_c_valor"]=(self.padre.antecedentesliquidacion.entryCajaValor.get_text())
			
			sql="""insert into antecedente_liquidacion 
			("""+",".join(["%s" %(n1) for n1,n2 in antecedente_liquidacion.iteritems()])+""") 
			VALUES
			("""+ ",".join(["'%s'" %(n2) for n1,n2 in antecedente_liquidacion.iteritems()])+")"
			#print sql
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
		#se destruye finingresartrabajador
		if len(self.padre.wins) and self.padre.wins.has_key("Fin ingresar trabajador"):
				self.padre.notebookMain.remove_page(3)
				del self.padre.wins["Fin ingresar trabajador"]
				self.padre.ingresarseleccionar.on_toolbuttonNuevo_clicked()
				self.padre.notebookMain.set_current_page(0)
				self.padre.antecedentesliquidacion.notebook1.set_current_page(0)
				self.padre.antecedentesliquidacion.notebook2.set_current_page(0)
		self.padre.ingresarseleccionar.lista_datos()
		
	def on_toolbuttonAtras_clicked(self, toolbuttonAtras=None):
		self.padre.notebookMain.prev_page()
