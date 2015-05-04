#!/bin/sh

wget http://standards.ieee.org/regauth/oui/oui.txt
if [ -f oui.txt ]
then
	cat oui.txt | grep "(hex)" | awk '{gsub("-",":",$1);  print $0}' | sed 's/ (hex) /#/' > MACs.goy
	rm -rf oui.txt
else
	echo
	echo "No se ha podido descargar el archivo \"oui.txt\"."
	echo "Es necesario disponer de conexión a internet."
	echo
	exit 1
fi
exit 0


