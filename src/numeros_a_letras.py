#!/usr/bin/env python
#-*- coding: latin1 -*-

############################################################################
#    Copyright (C) 2005 by												   #
#                                                                          #
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


_n1 = ( "un","dos","tres","cuatro","cinco","seis","siete","ocho",
        "nueve","diez","once","doce","trece","catorce","quince",
        "dieciséis","diecisiete","dieciocho","diecinueve","veinte")

_n11 =( "un","dós","trés","cuatro","cinco","séis","siete","ocho","nueve")

_n2 = ( "dieci","veinti","treinta","cuarenta","cincuenta","sesenta",
        "setenta","ochenta","noventa")

_n3 = ( "ciento","dosc","tresc","cuatroc","quin","seisc",
        "setec","ochoc","novec")

def numerals(nNumero, lFemenino=False):
    """
    numerals(nNumero, lFemenino) --> cLiteral

    Convierte el número a una cadena literal de caracteres
    P.e.:       201     -->   "doscientos uno"
               1111     -->   "mil ciento once"

    <nNumero>       Número a convertir
    <lFemenino>     = 'true' si el Literal es femenino
                    P.e.:   201     -->    "doscientas una"
    """
    # Nos aseguramos del tipo de <nNumero>
    # se podría adaptar para usar otros tipos (pe: float)
    nNumero = long(nNumero)

    if nNumero<0:       cRes = "menos "+numerals(-nNumero,lFemenino)
    elif nNumero==0:    cRes = "cero"
    else:               cRes = _numerals(nNumero,lFemenino)

    # Excepciones a considerar
    if not lFemenino and nNumero%10 == 1 and nNumero%100!=11:
        cRes += "o"

    return cRes


# Función auxiliar recursiva
def _numerals(n, lFemenino=False):

    # Localizar los billones    
    prim,resto = divmod(n,10L**12)
    if prim!=0:
        if prim==1:     cRes = "un billón"
        else:           cRes = _numerals(prim,0)+" billones" # Billones es masculino

        if resto!=0:    cRes += " "+_numerals(resto,lFemenino)

    else:
    # Localizar millones
        prim,resto = divmod(n,10**6)
        if prim!=0:
            if prim==1: cRes = "un millón"
            else:       cRes = _numerals(prim,0)+" millones" # Millones es masculino

            if resto!=0: cRes += " " + _numerals(resto,lFemenino)

        else:
    # Localizar los miles
            prim,resto = divmod(n,10**3)
            if prim!=0:
                if prim==1: cRes="mil"
                else:       cRes=_numerals(prim,lFemenino)+" mil"

                if resto!=0: cRes += " " + _numerals(resto,lFemenino)

            else:
    # Localizar los cientos
                prim,resto=divmod(n,100)
                if prim!=0:
                    if prim==1:
                        if resto==0:        cRes="cien"
                        else:               cRes="ciento"
                    else:
                        cRes=_n3[prim-1]
                        if lFemenino:       cRes+="ientas"
                        else:               cRes+="ientos"

                    if resto!=0:  cRes+=" "+_numerals(resto,lFemenino)

                else:
    # Localizar las decenas
                    if lFemenino and n==1:              cRes="una"
                    elif n<=20:                         cRes=_n1[n-1]
                    else:
                        prim,resto=divmod(n,10)
                        cRes=_n2[prim-1]
                        if resto!=0:
                            if prim==2:                 cRes+=_n11[resto-1]
                            else:                       cRes+=" y "+_n1[resto-1]

                            if lFemenino and resto==1:  cRes+="a"
    return cRes
