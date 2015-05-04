#!/bin/bash
CLAVES=10000000000
CRUNCH="software/./crunch"
if [ "$1" = "" ] #si no se pasa ningún parámetro se empieza desde el principio
then
	"$CRUNCH" 10 10 0123456789 2>/dev/null
else #sinó se continúa desde la contraseña indicada
	"$CRUNCH" 10 10 0123456789 -s "$1" 2>/dev/null
fi
