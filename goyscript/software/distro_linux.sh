#!/bin/sh

DISTRO=$(uname -n)

case "$DISTRO" in
wifislax)
	DISTRO="Wifislax";;
OpenWrt)
	DISTRO="OpenWrt";;
wifiway)
	DISTRO="Wifiway";;
this)
	DISTRO="Ubuntu"
	ln -s /lib/i386-linux-gnu/libssl.so.1.0.0 /lib/i386-linux-gnu/libssl.so.1 >/dev/null 2>&1
	ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/i386-linux-gnu/libcrypto.so.1 >/dev/null 2>&1;;
bt)
	DISTRO="Backtrack"
	ln -s /lib/libssl.so.0.9.8 /lib/libssl.so.1 >/dev/null 2>&1
	ln -s /lib/libcrypto.so.0.9.8 /lib/libcrypto.so.1 >/dev/null 2>&1
	ln -s /usr/lib/libpcap.so.1.0.0 /usr/lib/libpcap.so.1 >/dev/null 2>&1;;
kali)
	DISTRO="Kali Linux"
	ln -s /usr/lib/i386-linux-gnu/libpcap.so.0.8 /lib/libpcap.so.1 >/dev/null 2>&1
	ln -s /usr/lib/i386-linux-gnu/i686/cmov/libssl.so.1.0.0 /usr/lib/i386-linux-gnu/i686/cmov/libssl.so.1 >/dev/null 2>&1
	ln -s /usr/lib/i386-linux-gnu/i686/cmov/libcrypto.so.1.0.0 /usr/lib/i386-linux-gnu/i686/cmov/libcrypto.so.1 >/dev/null 2>&1;;
debian|debian7)
	DISTRO="Debian"
	ln -s /usr/lib/i386-linux-gnu/libpcap.so.0.8 /lib/libpcap.so.1 >/dev/null 2>&1
	ln -s /usr/lib/i386-linux-gnu/i686/cmov/libssl.so.1.0.0 /usr/lib/i386-linux-gnu/i686/cmov/libssl.so.1 >/dev/null 2>&1
	ln -s /usr/lib/i386-linux-gnu/i686/cmov/libcrypto.so.1.0.0 /usr/lib/i386-linux-gnu/i686/cmov/libcrypto.so.1 >/dev/null 2>&1;;
backbox)
	DISTRO="BackBox Linux"
	ln -s /lib/i386-linux-gnu/libssl.so.1.0.0 /lib/i386-linux-gnu/libssl.so.1 >/dev/null 2>&1
	ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/i386-linux-gnu/libcrypto.so.1 >/dev/null 2>&1;;
linux.site)
	DISTRO="openSUSE";;
archiso)
	DISTRO="Archlinux";;
awireless)
	DISTRO="AWireless";;
Microknoppix)
	DISTRO="KNOPPIX";;
*)
	ln -s /lib/libssl.so.0.9.8 /lib/libssl.so.1 > /dev/null 2>&1
	ln -s /lib/libcrypto.so.0.9.8 /lib/libcrypto.so.1 > /dev/null 2>&1
	ln -s /usr/lib/libpcap.so.1.0.0 /usr/lib/libpcap.so.1 > /dev/null 2>&1
	DISTRO="<Desconocida>";;
esac
echo "$DISTRO"
