#!/bin/sh

#COLORES
negro="\033[0;30m"
rojo="\033[0;31m"
verde="\033[0;32m"
marron="\033[0;33m"
azul="\033[0;34m"
magenta="\033[0;35m"
cyan="\033[01;36m"
grisC="\033[0;37m"
gris="\033[1;30m"
rojoC="\033[1;31m"
verdeC="\033[1;32m"
amarillo="\033[1;33m"
azulC="\033[1;34m"
magentaC="\033[1;35m"
cyanC="\033[1;36m"
blanco="\033[1;37m"
subrayar="\E[4m"
parpadeoON="\E[5m"
normal="\E[0m"
resaltar="\033[1;37m\E[7m"

COLOR="$amarillo"
CRONOMETRO="0:00:00   "
CARACTERES=${#CRONOMETRO}
echo -en $COLOR"$CRONOMETRO$normal\c"
ATAQUE_FUNCIONANDO=`ps -A | grep -e aircrack-ng -e pyrit`
while [ "$ATAQUE_FUNCIONANDO" = "" ]
do
	ATAQUE_FUNCIONANDO=`ps -A | grep -e aircrack-ng -e pyrit`
	sleep 0.01
done
let SEGUNDOS1=`date +%s`
while [ "$ATAQUE_FUNCIONANDO" != "" ]
do
	let SEGUNDOS2=`date +%s`
	let SEGUNDOS=$SEGUNDOS2-$SEGUNDOS1
	let HORAS=`expr $SEGUNDOS / 3600`
	let SEGUNDOS=`expr $SEGUNDOS % 3600`
	let MINUTOS=`expr $SEGUNDOS / 60`
	let SEGUNDOS=`expr $SEGUNDOS % 60`
	ATAQUE_FUNCIONANDO=`ps -A | grep -e aircrack-ng -e pyrit`
	if [ "$ATAQUE_FUNCIONANDO" = "" ]
	then
		exit 0
	else
		sleep 1
	fi
	echo -ne "\033[${CARACTERES}D" #situa el cursor al principio del texto
	CRONOMETRO=`printf "%d:%02d:%02d   " $HORAS $MINUTOS $SEGUNDOS`
	CARACTERES=${#CRONOMETRO}
	echo -en $COLOR"$CRONOMETRO$normal\c"
done
