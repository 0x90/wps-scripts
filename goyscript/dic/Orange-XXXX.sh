#!/bin/bash
CLAVES=214358881
#################################################################
# -*- ENCODING: UTF-8 -*-                                       #
# Este programa es software libre. Puede redistribuirlo y/o     #
# modificar-lo bajo los términos de la Licencia Pública General #
# de GNU según es publicada por la Free Software Foundation,    #
# bien de la versión 3 de dicha Licencia o bien (según su       #
# elección) de cualquier versión posterior.                     #
#                                                               #
# Si usted hace alguna modificación en esta aplicación,         #
# deberá siempre mencionar al autor original de la misma.       #
#                                                               #
# Autor: GOYfilms                                               #
# Basado en el algoritmo de generación de contraseñas de:       #
#   Orange.sh publicado en lampiweb.com                         #
# Autor del script original:                                    #
#   1camaron1 with the collaboration of kcdtv                   #
#################################################################
# MACs afectadas:
#   1C:C6:3C
#   50:7E:5D
#   74:31:70
#   84:9C:A6
#   88:03:55

CRUNCH="software/./crunch"

if [ "$1" = "" ] #si no se pasan parámetros
then
	"$CRUNCH" 8 8 4A59E3F6C27 2>/dev/null
else #si se pasa como parámetro la última contraseña probada continúa desde ahí
	"$CRUNCH" 8 8 4A59E3F6C27 -s "$1" 2>/dev/null
fi
