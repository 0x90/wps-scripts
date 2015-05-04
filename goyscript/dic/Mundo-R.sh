#!/bin/bash
CLAVES=3000000
CRUNCH="software/./crunch"
let CARACTERES="${#1}" #nº caracteres de la última contraseña probada

function error
{
echo
echo "ERROR"
echo
sleep 5
exit 1
}


if [ $CARACTERES -eq 0 ] #si no se pasó ningún parámetro
then
	"$CRUNCH" 8 8 0123456789 -t 20%%%%%% 2>/dev/null
	"$CRUNCH" 8 8 0123456789 -t 06%%%%%% 2>/dev/null
	"$CRUNCH" 13 13 0123456789 -t %%%%%%0000000 2>/dev/null
else #si se pasó algún parámetro
	if [ $CARACTERES -eq 8 ] #si el parámetro tiene 8 caracteres (tipo1 o tipo2)
	then
		INICIO=`echo "$1" | cut -c-2` #los dos primeros dígitos de la última contraseña probada
		if [ "$INICIO" = "20" ] #si es tipo1
		then
			"$CRUNCH" 8 8 0123456789 -t 20%%%%%% -s "$1" 2>/dev/null
			"$CRUNCH" 8 8 0123456789 -t 06%%%%%% 2>/dev/null
			"$CRUNCH" 13 13 0123456789 -t %%%%%%0000000 2>/dev/null
		else
			if [ "$INICIO" = "06" ] #si es tipo2
			then
				"$CRUNCH" 8 8 0123456789 -t 06%%%%%% -s "$1" 2>/dev/null
				"$CRUNCH" 13 13 0123456789 -t %%%%%%0000000 2>/dev/null
			else
				error
			fi
		fi
	else
		if [ $CARACTERES -eq 13 ] #si el parámetro tiene 13 caracteres (tipo3)
		then
			"$CRUNCH" 13 13 0123456789 -t %%%%%%0000000 -s "$1" 2>/dev/null
		else
			error
		fi
	fi
fi
