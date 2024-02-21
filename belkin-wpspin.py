#!/usr/bin/env python

'''
Created on Dec 9, 2012

@author     : e.novellalorente@student.ru.nl

Original work : ZhaoChunsheng 04/07/2012

'''

import sys

VERSION = 0
SUBVERSION = 2

def usage():
    print("[+] WPSpin %d.%d " % (VERSION, SUBVERSION))
    print("[*] Usage : python WPSpin.py 123456")
    sys.exit(0)

def wps_pin_checksum(pin):
    accum = 0
    while(pin):
        accum += 3 * (pin % 10)
        pin //= 10  # Change to ensure integer division
        accum += pin % 10
        pin //= 10  # Change to ensure integer division
    return (10 - accum % 10) % 10

try:
    if (len(sys.argv[1]) == 6):
        p = int(sys.argv[1], 16) % 10000000
        print("[+] WPS pin is : %07d%d" % (p, wps_pin_checksum(p)))
    else:
        usage()
except IndexError:  # Handles missing sys.argv[1]
    usage()
except ValueError:  # Handles invalid int conversion
    usage()
