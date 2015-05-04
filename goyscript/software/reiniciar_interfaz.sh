#!/bin/sh
#SCRIPT QUE REINICIA UNA INTERFAZ DE RED PASADA COMO PARÁMETRO
cyanC="\033[1;36m"
grisC="\033[0;37m"
blanco="\033[1;37m"
INTERFAZ="$1"
DRIVER=`ls -l /sys/class/net/$INTERFAZ/device/driver | awk -F '/' '{print $NF}'`
echo -e $cyanC"Reiniciando la interfaz $blanco$INTERFAZ $grisC($DRIVER)$cyanC..."
echo -e $grisC
rmmod -f "$DRIVER" >/dev/null 2>&1 #reiniciamos la interfaz
if [ "$DRIVER" = "ath9k_htc" ]
then
	ifconfig $INTERFAZ >/dev/null 2>&1
	while [ $? -eq 0 ] #esperamos a que se desactive el módulo de la interfaz
	do
		ifconfig $INTERFAZ >/dev/null 2>&1
	done
fi
modprobe "$DRIVER" >/dev/null 2>&1
if [ "$DRIVER" = "ath9k_htc" ]
then
	ifconfig $INTERFAZ >/dev/null 2>&1
	while [ $? -ne 0 ] #esperamos a que se active el módulo de la interfaz
	do
		ifconfig $INTERFAZ >/dev/null 2>&1
	done
fi
exit 0
