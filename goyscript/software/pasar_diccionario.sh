#!/bin/sh

# $1=Diccionario
# $2=Parámetros del script (si procede)
# $3=aircrack-ng o pyrit
# $4=handshake
# $5=archivo .txt donde se guardará la contraseña
# $6=MAC del AP

SAVER="software/Saver" #programa creado por Coeman76 (muchísimas gracias por el aporte)
DIC="dic"
TMP="tmp"
ULTIMA_PROBADA="" #inicializamos la variable (por si no hubiera sesión previa)
let PROBADAS=1 #inicializamos la variable (por si no hubiera sesión previa)
let MARGEN_AIRCRACK=8000 #cuantas contraseñas se dejan de margen para compensar el buffer de aircrack
let MARGEN_PYRIT=80000 #cuantas contraseñas se dejan de margen para compensar el buffer de pyrit
CARPETA_SESIONES="wpa/sesiones"
SESION_SAVER=`echo "$4" | sed 's/.cap$//' | awk -F '/' '{print $NF}'` #nombre del archivo de captura sin extensión ni ruta
SESION_SAVER=`echo "$CARPETA_SESIONES/$SESION_SAVER"`
NOMBRE_DICCIONARIO=`echo "$1" | awk -F '/' '{print $NF}' | sed 's/.sh$//' | sed 's/.dic$//' | sed 's/.txt$//'` #nombre del diccionario sin extensión ni ruta
SESION_SAVER="$SESION_SAVER[$NOMBRE_DICCIONARIO]"
mkdir -p "$DIC" > /dev/null 2>&1
mkdir -p "$TMP" > /dev/null 2>&1
mkdir -p "$CARPETA_SESIONES" > /dev/null 2>&1
rm -rf "$TMP/FINALIZADO.tmp" > /dev/null 2>&1

control_c()
{
if [ $PROBADAS -ne 0 ]
then
	let PROBADAS_ESTA_SESION=`sed -n 7p "$SESION_SAVER".sav`
	let PROBADAS=$PROBADAS+$PROBADAS_ESTA_SESION
	sed -i "7c$PROBADAS" "$SESION_SAVER".sav #reemplaza la línea 7 con el valor actualizado
fi
}

### PROGRAMA PRINCIPAL ###

trap control_c SIGINT

TIPO_DICCIONARIO=`echo "$1" | grep '.sh$'`
if [ -f "$SESION_SAVER".sav ] #si hay una sesión anterior guardamos el número de contraseñas probadas para sumarlas al final de ésta
then
	ULTIMA_PROBADA=`sed -n 4p "$SESION_SAVER".sav`
	let PROBADAS=`sed -n 7p "$SESION_SAVER".sav`
fi
if [ "$TIPO_DICCIONARIO" = "" ] #si se trata de un diccionario de texto plano ".dic" o ".txt"
then
	PROGRAMA=`echo "$3" | grep "aircrack-ng"`
	if [ "$PROGRAMA" != "" ] #se usa aircrack
	then
		sed -n ${PROBADAS},99999999999999p "$1" | $SAVER $MARGEN_AIRCRACK "$SESION_SAVER".sav | "$3" -0 -w - -b "$6" -l "$5" "$4"
	else
		PROGRAMA=`echo "$3" | grep "pyrit"`
		if [ "$PROGRAMA" != "" ] #se usa pyrit
		then
			sed -n ${PROBADAS},99999999999999p "$1" | $SAVER $MARGEN_PYRIT "$SESION_SAVER".sav | "$3" -r "$4" -o "$5" -b "$6" -i - attack_passthrough
		fi
	fi
else #si se trata de un script ".sh"
	PROGRAMA=`echo "$3" | grep "aircrack-ng"`
	if [ "$PROGRAMA" != "" ] #se usa aircrack
	then
		"$1" "$2" | $SAVER $MARGEN_AIRCRACK "$SESION_SAVER".sav | "$3" -0 "$4" -l "$5" -b "$6" -w -
	else
		PROGRAMA=`echo "$3" | grep "pyrit"`
		if [ "$PROGRAMA" != "" ] #se usa pyrit
		then
			"$1" "$2" | $SAVER $MARGEN_PYRIT "$SESION_SAVER".sav | "$3" -r "$4" -o "$5" -b "$6" -i - attack_passthrough
		fi
	fi
fi
if [ ! -f "$SESION_SAVER".sav ] #si no existe la sesión (cuando se acaba de pasar un diccionario Saver borra la sesión)
then
	echo -n > "$TMP/FINALIZADO.tmp" #Se crea una baliza para confirmar que se terminó de pasar el diccionario
fi
killall -q aircrack-ng pyrit > /dev/null 2>&1
