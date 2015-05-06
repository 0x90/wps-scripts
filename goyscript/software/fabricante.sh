#!/bin/sh
#by GOYfilms

if [ -f "MACs.goy" ] #por si se ejecuta el script desde el directorio del mismo
then
	MACS="MACs.goy"
else
	if [ -f "software/MACs.goy" ] #por si se ejecuta el script desde goyscript
	then
		MACS="./software/MACs.goy"
	else
		echo "No se encuentra la base de datos"
		exit 1
	fi
fi

MAC_MITAD=`echo "$1" | cut -c-8` #guarda los 3 primeros pares de la MAC pasada como parámetro
FABRICANTE=`grep "$MAC_MITAD" $MACS | awk -F '#' '{print $2}'`
let LINEAS=`echo "$FABRICANTE" | wc -l`
if [ "$FABRICANTE" = "" ]
then
	FABRICANTE="< desconocido >"
else
	if [ $LINEAS -ne 1 ]
	then
		FABRICANTE="< ERROR >"
	fi
fi
echo "$FABRICANTE"
