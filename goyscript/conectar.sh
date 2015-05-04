#!/bin/sh

##### CONSTANTES #####
AIRMON="./software/airmon-ng"
WPA_PSK_RAW="./software/wpa_passphraseMOD" # modificación de wpa_passphrase para que no compruebe la longitud de la contraseña (y en español ;-D)CLAVES="claves"
MACS="./software/MACs.goy"
CLAVES="claves"
TEMP="tmp"
VERSION=`cat VERSION`

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
parpadeoOFF="\E[0m"
resaltar="\E[7m"

#NOMBRE Y VERSIÓN DEL SCRIPT
version()
{
SCRIPT=" Conectar $VERSION by GOYfilms "
N_SCRIPT=${#SCRIPT}
N_VERSION=${#VERSION}
let CARACTERES=$N_SCRIPT*3
LINEA=`echo "══════════════════════════════════════════" | cut -c-${CARACTERES}`
clear
echo -e "$blanco\c"
echo -e "╔${LINEA}╗"
echo -e "║${SCRIPT}║"
echo -e "╚${LINEA}╝"
echo -e $grisC
}

#DETIENE POSIBLES PROCESOS EN MARCHA
matar_procesos()
{
echo -e "$cyan""\n$1"
echo -e "$grisC"
PROCESOS=`ps -A | grep -e xterm -e ifconfig -e dhcpcd -e dhclient -e NetworkManager -e wpa_supplicant -e udhcpc`
while [ "$PROCESOS" != "" ]
do
	killall -q xterm ifconfig dhcpcd dhclient dhclient3 NetworkManager wpa_supplicant udhcpc > /dev/null 2>&1
	PROCESOS=`ps -A | grep -e xterm -e ifconfig -e dhcpcd -e dhclient -e NetworkManager -e wpa_supplicant -e udhcpc`
done
desactivar_todos_monX
}

#SELECCIÓN DE LA TARJETA WiFi
seleccionar_tarjeta()
{
TARJETAS_WIFI_DISPONIBLES=`iwconfig --version | grep "Recommend" | awk '{print $1}' | sort`
N_TARJETAS_WIFI=`echo $TARJETAS_WIFI_DISPONIBLES | awk '{print NF}'`
if [ "$TARJETAS_WIFI_DISPONIBLES" = "" ]
then
	echo -e ""$rojoC"ERROR: No se detectó ninguna tarjeta WiFi"
	echo -e "$grisC"
else
	echo -e ""$cyan"Tarjetas WiFi disponibles:"$grisC""
	echo
	let CONT=1
	while [ $CONT -le $N_TARJETAS_WIFI ]
	do
		INTERFAZ=`echo $TARJETAS_WIFI_DISPONIBLES | awk '{print $'$CONT'}'`
		DRIVER=`ls -l /sys/class/net/$INTERFAZ/device/driver | sed 's/^.*\/\([a-zA-Z0-9_-]*\)$/\1/'`
		MAC=`ifconfig "$INTERFAZ" | grep -oE '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' | awk '{print toupper($0)}' | cut -c-8` #extraemos la MAC XX:XX:XX (sólo los 3 primeros pares)
		FABRICANTE_INTERFAZ=`grep $MAC $MACS | awk -F '#' '{print $2}'`
		if [ "$FABRICANTE_INTERFAZ" = "" ]
		then
			FABRICANTE_INTERFAZ="<Desconocido>"
		fi
		if [ $CONT -eq 1 ]
		then
			echo -e ""$cyan" Nº\tINTERFAZ\tDRIVER\t\tFABRICANTE"
			echo -e ""$cyan" ══\t════════\t══════\t\t══════════"
		fi
		CARACTERES_DRIVER=`echo $DRIVER | wc -c` 
		if [ $CARACTERES_DRIVER -gt 8 ] #CONTROLA LA TABULACIÓN DEPENDIENDO DE LOS CARACTERES QUE TENGA LA VARIABLE "DRIVER"
		then
			TAB=""
		else
			TAB="\t"
		fi
		echo -e ""$amarillo" $CONT)\t$INTERFAZ \t\t$DRIVER\t"$TAB"$FABRICANTE_INTERFAZ"
		let CONT=$CONT+1
	done
	if [ $N_TARJETAS_WIFI -gt 1 ] # SI DETECTA MAS DE UNA NOS PREGUNTA CUAL QUEREMOS
	then
		echo -e "\n"$cyan"\nSelecciona una tarjeta WiFi:\c"
		echo -e ""$amarillo" \c"
		read -n 1 OPCION
		while [[ $OPCION < 1 ]] || [[ $OPCION > $N_TARJETAS_WIFI ]]
		do
			echo -en "\a\033[10C"$rojoC"OPCIÓN NO VÁLIDA"$grisC""
			echo -en ""$cyan"\rSelecciona una tarjeta WiFi: "$amarillo"\c"
			read -n 1 OPCION
		done
	else
		OPCION=1
	fi
	echo -en "\a\033[10C                "$grisC"" #BORRA EL MENSAJE DE "OPCIÓN NO VÁLIDA"
fi
if [ $N_TARJETAS_WIFI -gt 1 ] # SI DETECTA MÁS DE UNA VARÍA EL MENSAJE
then
	INTERFAZ=`echo $TARJETAS_WIFI_DISPONIBLES | awk '{print $'$OPCION'}'`
	echo -e "\n"
	echo -e ""$cyan"Has seleccionado: "$verdeC"$INTERFAZ"$grisC""
	echo
else
	echo
	echo -e ""$cyan"Sólo se ha detectado una tarjeta WiFi: "$verdeC"$INTERFAZ"$grisC""
	echo
fi
}

#SELECCIONA UNA RED DE LA LISTA
seleccionar_red()
{
if [ "$FILTRAR" = "SI" ]
then
	find $CLAVES | grep .txt | grep "$FILTRO" | sort | sed 's#^'"$CLAVES"'/##' > "$TEMP/redes.menu"
else
	find $CLAVES | grep .txt | sort | sed 's#^'"$CLAVES"'/##' > "$TEMP/redes.menu"
fi
echo -e $cyanC"  Nº RED"
echo -e $cyanC"  ══ ═════════════════════════════"
let CONT=1
let LINEAS=`cat "$TEMP/redes.menu" | wc -l`
while [ $CONT -le $LINEAS ]
do
	RED=`sed -n ${CONT}p "$TEMP/redes.menu"`
	if [ $CONT -gt 99 ]
	then
		ESPACIO=""
	else
		if [ $CONT -gt 9 ]
		then
			ESPACIO=" "
		else
			ESPACIO="  "
		fi
	fi
	echo -e $blanco"$ESPACIO$CONT) $RED"
	let CONT=$CONT+1
done
echo -e $grisC
echo -e ""$cyan"\rSelecciona una red de la lista: "$amarillo"\c"
read OPCION
while [[ $OPCION -lt 1 ]] || [[ $OPCION -gt $LINEAS ]]
do
	echo -en "\a\033[1A\033[37C"$rojoC"OPCIÓN NO VÁLIDA \033[K"$grisC""
	sleep 1
	echo -en "\a\r"$cyan"Selecciona una red de la lista: \033[K"$amarillo"\c"
	read OPCION
done
echo -e ""$cyan"\033[1ASelecciona una red de la lista: "$amarillo"$OPCION\033[K"
RUTA_COMPLETA=`sed -n ${OPCION}p "$TEMP/redes.menu"`
ARCHIVO=`echo "$RUTA_COMPLETA" | awk -F '/' '{print $NF}'`
MAC_GUIONES=`echo "$ARCHIVO" | awk -F '(' '{print $NF}' | awk -F ')' '{print $1}'`
let CARACTERES=`echo "$ARCHIVO" | wc -c`
let CARACTERES=$CARACTERES-25
NOMBRE_AP=`echo "$ARCHIVO" | cut -c-${CARACTERES}`
}

#COMPRUEBA SI HAY INTERFACES EN MODO MONITOR Y, SI LAS HAY, LAS DESACTIVA
desactivar_todos_monX()
{
INTERFACES_MONITOR=`iwconfig --version | grep "Recommend" | awk '{print $1}' | grep mon`
if [ "$INTERFACES_MONITOR" != "" ]
then
	echo -e $cyanC"Desactivando modo monitor..."
	echo -e $grisC
fi
let CUANTAS=`echo "$INTERFACES_MONITOR" | wc -l`
let CONT=1
while [ $CONT -le $CUANTAS ]
do
	MON=`echo $INTERFACES_MONITOR | awk '{print $'$CONT'}'`
	$AIRMON stop $MON > /dev/null 2>&1
	let CONT=$CONT+1
done
}

#SE CONECTA A LA RED SELECCIONADA CON LA CONTRASEÑA GUARDADA
conectar_internet()
{
echo -e "$cyan\n"
echo -e "Configurando la tarjeta WiFi para conectarse a la red \"$NOMBRE_AP\"..."$grisC""
echo
killall -q dhcpcd dhclient udhcpc wpa_supplicant > /dev/null 2>&1
desactivar_todos_monX
LINEAS_CLAVE=$(cat "./$CLAVES/$RUTA_COMPLETA" | wc -l)
if [ $LINEAS_CLAVE -eq 2 ] #SI EL TXT QUE CONTIENE LA CONTRASEÑA TIENE 2 LINEAS ES PORQUE SE DESENCRIPTÓ CON goyscriptWPS sinó con goyscriptWPA
then
	CLAVE_WPA=$(cat "./$CLAVES/$RUTA_COMPLETA" | sed -n 2p | awk -F "'" '{print $2}')
else
	CLAVE_WPA=$(cat "./$CLAVES/$RUTA_COMPLETA")
fi
$WPA_PSK_RAW "$NOMBRE_AP" "$CLAVE_WPA" > "$TEMP/internet.conf"
wpa_supplicant -B -D wext -i $INTERFAZ -c "$TEMP/internet.conf" >/dev/null 2>&1
sleep 1
echo -e ""$cyan"Iniciando cliente DHCP. Puede llevar un tiempo, ten paciencia..."$grisC"\n"
which dhclient > /dev/null 2>&1
if [ $? -eq 0 ]
then
	dhclient -r
	dhclient $INTERFAZ
else
	which dhcpcd > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		dhcpcd $INTERFAZ > /dev/null 2>&1
	else
		echo -e $rojoC"No se ha encontrado ningún cliente DHCP instalado."
		echo -e $rojoC"No se ha podido realizar la conexión."
		echo -e $grisC
		matar_procesos "Cerrando los procesos abiertos..."
		pulsar_una_tecla "Pulsa una tecla para salir..."
	fi
fi
if [ $? -ne 0 ] #SI NO VA A LA SEGUNDA NO CREO QUE VAYA BIEN LA COSA :D
then
	echo -e "$rojoC"
	echo "No ha sido posible realizar la conexión."
	echo "Probablemente estás demasiado lejos del punto de acceso."
	echo -e "$grisC"
else
	echo -e $verdeC"Configuración finalizada. Comprueba si tienes conexión."
	echo -e "$grisC"
	which firefox > /dev/null 2>&1
	if [ $? -eq 0 ]
	then
		$(which firefox) www.google.es >/dev/null 2>&1 &
		echo -e "$verdeC"
		echo "Abriendo \"Firefox\"..."
		echo -e "$grisC"
	else
		which konqueror > /dev/null 2>&1
		if [ $? -eq 0 ]
		then
			$(which konqueror) www.google.es >/dev/null 2>&1 &
			echo -e "$verdeC"
			echo "Abriendo \"Konqueror\"..."
			echo -e "$grisC"
		else
			echo -e $rojoC"No tienes instalado \"Firefox\" ni \"Konqueror\"."
			echo -e "Si tienes algún otro navegador ejecútalo."
			echo -e $grisC
		fi
	fi
	echo -en $blanco"Pulsa \"D\" para desconectarte de $cyanC\"$NOMBRE_AP\"$blanco... $amarillo"
	read -n 1 TECLA
	while [[ "$TECLA" != "D" ]] && [[ "$TECLA" != "d" ]]
	do
		echo -en $rojoC"      OPCIÓN NO VÁLIDA  "
		sleep 1
		echo -en $blanco"\rPulsa \"D\" para desconectarte de $cyanC\"$NOMBRE_AP\"$blanco... $amarillo\033[K"
		read -n 1 TECLA
	done
	echo -e $grisC
	matar_procesos "Desconectando de $blanco\"$NOMBRE_AP\"$cyanC..."
fi
}

##### PROGRAMA PRINCIPAL #####

version
mkdir -p "$TEMP" > /dev/null 2>&1
if [ "$1" = "" ]
then
	FILTRAR="NO"
else
	FILTRAR="SI"
	FILTRO="$1"
fi
desactivar_todos_monX
seleccionar_tarjeta
seleccionar_red
conectar_internet

#FIN
