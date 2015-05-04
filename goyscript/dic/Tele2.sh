#!/bin/bash
CLAVES=20000000
CRUNCH="software/./crunch"
let CARACTERES="${#1}" #nº caracteres de la última contraseña probada

if [ $CARACTERES -eq 0 ] #si son 0 caracteres es que no se pasó ningún parámetro (no hay sesión)
then
	"$CRUNCH" 11 11 0123456789 -t IX1V%%%%%%% 2>/dev/null
	"$CRUNCH" 13 13 0123456789 -t IX1VPV%%%%%%% 2>/dev/null
else
	if [ $CARACTERES -eq 11 ] #si son 11 caracteres se continuará la primera parte
	then
		"$CRUNCH" 11 11 0123456789 -t IX1V%%%%%%% -s "$1" 2>/dev/null
		"$CRUNCH" 13 13 0123456789 -t IX1VPV%%%%%%% 2>/dev/null
	else
		if [ $CARACTERES -eq 13 ] #si son 13 caracteres se continuará la segunda parte
		then
			"$CRUNCH" 13 13 0123456789 -t IX1VPV%%%%%%% -s "$1" 2>/dev/null
		else #si no es ninguno de los casos anteriores... algo se hizo mal :(
			echo
			echo "ERROR"
			echo
			sleep 5
		fi
	fi
fi
