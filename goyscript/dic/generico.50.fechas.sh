#!/bin/bash
CLAVES=751812

function error
{
echo
echo "ERROR"
echo
sleep 5
exit 1
}


if [ "$1" = "" ] #si no se indica cual es la última contraseña probada
then
	let DIA=1
	let MES=1
	let ANO=0
else
	let CARACTERES="${#1}"
	if [ $CARACTERES -eq 8 ] #si el parámetro tiene 8 caracteres
	then
		let DIA=`echo "$1" | awk -F "" '{print $1$2}' | sed 's/^0//'`
		let MES=`echo "$1" | awk -F "" '{print $3$4}' | sed 's/^0//'`
		let ANO=`echo "$1" | awk -F "" '{print $5$6$7$8}' | sed 's/^0//'`
	else
		error
	fi
fi
while [ $ANO -le 2020 ]
do
	printf '%02d%02d%04d\n' $DIA $MES $ANO
	let DIA=$DIA+1
	if [ $DIA -gt 31 ]
	then
		let DIA=1
		let MES=$MES+1
	fi
	if [ $MES -gt 12 ]
	then
		let MES=1
		let ANO=$ANO+1
	fi
done

