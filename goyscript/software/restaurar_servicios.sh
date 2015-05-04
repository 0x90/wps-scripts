#!/bin/sh
#SCRIPT QUE, AL CERRARSE GOYscript, DESACTIVA EL MODO MONITOR Y ACTIVA EL
#GESTOR DE CONEXIÓN SI PROCEDE
#SE PASA COMO PARÁMETRO EL PID DE GOYscript
TMP="tmp"
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
parpadeoOFF="\E[0m"
resaltar="\E[7m"

if [ -f "airmon-ng" ] #si airmon está en el directorio actual
then
	AIRMON="./airmon-ng"
else
	if [ -f "software/airmon-ng" ] #si está dentro de la carpeta "software"
	then
		AIRMON="software/./airmon-ng"
	fi
fi

#ESPERA A QUE SE CIERRE GOYscript para CONTINUAR
esperar_a_que_se_cierre_goyscript()
{
echo "$(date "+%d/%m/%Y %H:%M")  Esperando a que se cierre el proceso con PID $PID" >> "$TMP/restaurar_servicios.log"
FUNCIONANDO=`ps | grep "$PID"`
while [ "$FUNCIONANDO" != "" ]
do
	FUNCIONANDO=`ps | grep "$PID"`
	sleep 1
done
echo "$(date "+%d/%m/%Y %H:%M")  Proceso con PID $PID terminado" >> "$TMP/restaurar_servicios.log"
}

#MATA TODOS LOS PROCESOS RELACIONADOS CON GOYscript
matar_procesos()
{
echo "$(date "+%d/%m/%Y %H:%M")  Matando los procesos" >> "$TMP/restaurar_servicios.log"
PROCESOS=`ps | egrep -a -n '(goyscript_redes|ifconfig|dhcpcd|dhclient|NetworkManager|wpa_supplicant|udhcpc|airodump-ng|aireplay-ng|airbase-ng|aircrack-ng|airmon-ng|wash|reaver)'`
while [ "$PROCESOS" != "" ]
do
	killall -q goyscript_redes ifconfig dhcpcd dhclient NetworkManager wpa_supplicant udhcpc airodump-ng aireplay-ng airbase-ng aircrack-ng airmon-ng wash reaver >/dev/null 2>&1
	PROCESOS=`ps | egrep -a -n '(goyscript_redes|ifconfig|dhcpcd|dhclient|NetworkManager|wpa_supplicant|udhcpc|airodump-ng|aireplay-ng|airbase-ng|aircrack-ng|airmon-ng|wash|reaver)'`
done
}

#DESACTIVA EL MODO MONITOR EN TODAS LAS INTERFACES
desactivar_todos_monX()
{
echo "$(date "+%d/%m/%Y %H:%M")  Desactivando modo monitor" >> "$TMP/restaurar_servicios.log"
INTERFACES_MONITOR=`iwconfig --version | grep "Recommend" | awk '{print $1}' | grep mon`
let CUANTAS=`echo $INTERFACES_MONITOR | wc -w`
let CONT=1
while [ $CONT -le $CUANTAS ]
do
	MON=`echo $INTERFACES_MONITOR | awk '{print $'$CONT'}'`
	$AIRMON stop $MON > /dev/null 2>&1
	let CONT=$CONT+1
done
}

#INICIA WICD SI ESTÁ INSTALADO EN EL SISTEMA
iniciar_wicd()
{
echo "$(date "+%d/%m/%Y %H:%M")  Iniciando wicd" >> "$TMP/restaurar_servicios.log"
WICD_FUNCIONANDO=`ps -A | grep wicd`
if [ "$WICD_FUNCIONANDO" = "" ] #si wicd no se está ejecutando
then
	which wicd >/dev/null 2>&1
	if [ $? -eq 0 ] #si wicd está instalado (y en el path)
	then
		echo "$(date "+%d/%m/%Y %H:%M")  Iniciando servicio wicd" >> "$TMP/restaurar_servicios.log"
		wicd >/dev/null 2>&1 #lo ejecuta
	fi
	WICD_CLIENT_FUNCIONANDO=`ps -A | grep wicd-client`
	which wicd-client >/dev/null 2>&1
	if [ $? -eq 0 ] && [ "$KDE" = "" ] && [ "$WICD_CLIENT_FUNCIONANDO" = "" ] #si wicd está instalado (y en el path)
	then
		echo "$(date "+%d/%m/%Y %H:%M")  Iniciando cliente wicd" >> "$TMP/restaurar_servicios.log"
		nohup wicd-client --tray >/dev/null 2>&1 & #lo ejecuta
	fi
fi
}

#INICIA NetworkManager SI ESTÁ INSTALADO EN EL SISTEMA
iniciar_NetworkManager()
{
echo "$(date "+%d/%m/%Y %H:%M")  Iniciando NetworkManager" >> "$TMP/restaurar_servicios.log"
NETWORKMANAGER_FUNCIONANDO=`ps -A | grep NetworkManager`
if [ "$NETWORKMANAGER_FUNCIONANDO" = "" ] #si NetworkManager no se está ejecutando
then
	which NetworkManager >/dev/null 2>&1
	if [ $? -eq 0 ] #si NetworkManager está instalado (y en el path)
	then
		NetworkManager >/dev/null 2>&1 #lo ejecuta
	fi
fi
}


### PROGRAMA PRINCIPAL ###

rm -rf "$TMP/restaurar_servicios.log" >/dev/null 2>&1
INTERFAZ_GRAFICA=`ps | grep -e goyscriptTTY -e goyscriptWRT | grep -v grep`
if [ "$INTERFAZ_GRAFICA" = "" ]
then
	INTERFAZ_GRAFICA="SI"
	PID="$1"
	KDE=`ps -A | grep kded`
else
	INTERFAZ_GRAFICA="NO"
	PID=`ps -A | grep -e goyscriptTTY -e goyscriptWRT | grep -v grep | awk '{print $1}'`
fi
esperar_a_que_se_cierre_goyscript
matar_procesos
desactivar_todos_monX
if [ "$INTERFAZ_GRAFICA" = "SI" ]
then
	iniciar_wicd
	iniciar_NetworkManager
fi
echo "$(date "+%d/%m/%Y %H:%M")  Saliendo..." >> "$TMP/restaurar_servicios.log"
killall -q screen >/dev/null 2>&1
exit 0
