#!/bin/bash
CLAVES=4000000
PARAMETRO="$1"
CRUNCH="software/./crunch"
PREFIJOS='\
981
982
988
986'
let CUANTOS_PREFIJOS=`echo "$PREFIJOS" | wc -l`
if [ "$PARAMETRO" = "" ]
then
	let CONT=1
else
	PREF=`echo "$PARAMETRO" | cut -c-3` #extraemos el prefijo del último número pasado como parámetro
	let CONT=`echo "$PREFIJOS" | grep -n "$PREF" | awk -F ':' '{print $1}'`
fi

while [ $CONT -le $CUANTOS_PREFIJOS ]
do
	PREFIJO_ACTUAL=`echo "$PREFIJOS" | sed -n ${CONT}p`
	if [ "$PARAMETRO" != "" ] #si se pasó algún parámetro (=sesión anterior)
	then
		"$CRUNCH" 9 9 0123456789 -t $PREFIJO_ACTUAL%%%%%% -s "$PARAMETRO" 2>/dev/null
		PARAMETRO=""
	else
		"$CRUNCH" 9 9 0123456789 -t $PREFIJO_ACTUAL%%%%%% 2>/dev/null
	fi
	let CONT=$CONT+1
done
