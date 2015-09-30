# pyxiewps overview

Pyxiewps is a wireless attack tool written in python that uses reaver, pixiewps, macchanger and aircrack to retrieve the WPS pin of any vulnerable AP in seconds.
It's a wrapper.
It is meant for educational purposes only. All credits for the research go to Dominique Bongard.

It uses:
  Reaver: Reaver 1.5.2 mod by t6_x & DataHead & Soxrok2212 & Wiire & kib0rg
  Pixiewps: by wiire <wi7ire@gmail.com>
  Aircrack: http://www.aircrack-ng.org
  Macchanger: by Alvaro Lopez Ortega

There are already a bunch of tools, reaver included, that can attack an access point (AP) using the Pixie Dust vulnerability but I wanted to do something automatic, fast and user friendly, so here we are.

I also wrote this program to be used on the fly as I walk in the city. If the router is vulnerable, this script uses reaver and pixiewps to retrieve the AP password in, at least, 11 seconds. YUP! You get the WPA password of any vulnerable AP in 11 seconds using the fastest configuration.

It enumerates all the APs with active WPS, tries to get the PKE, PKR, E-NONCE, R-NONCE, AUTHKEY, HASH1 and 2 using the patched version of reaver, then passes all that information to pixiewps program so that it can retrieve the WPS pin, and finally runs reaver again with the pin that pixiewps found to get the AP WPA password.

Please report any bugs to pyxiewps@gmail.com ||
Twitter: https://twitter.com/jgilhutton ||
Demonstration: https://www.youtube.com/watch?v=1MOhqeYr3yU

# What's the Aircrack thing?

You can find two versions for each language. One of them uses Aircrack to set the interface into monitor mode and the other one doesn't. Just in case you wonder why, here is the explanation: Last version of aircrack works badly when it sets the monitor mode in some distros. The most frequent error is the SIOCSIFFLAGS one. This error does not stop Airmon to create the monitor interface so the script continues and it's not aware of this problem. That's why the only output that some users get is "No WPS-active APs were found." in less than 2 seconds because wash crashes at enumerating the APs and it's all in a whole try-except block of Python.
The solution was to modify the script to use these commands instead of Airmon:
	
	$ ifconfig <interface> down
	$ iwconfig <interface> mode monitor
	$ ifconfig <interface> up  # see "third party bugs"

# USAGE
  	python pyxiewps-[LANGUAGE].py <arguments>
  	
	-r --use-reaver          Use reaver to get all the AP information.              [False]
	-p --use-pixie           Once all the data is captured with reaver              [False]
	                         the script tries to get the WPS pin with pixiewps.
	-w --wash-time [time]    Set the time used to enumerate all the WPS-active APs. [15]
	-t --time [time]         Set the time used to get the hex data from the AP.       [6]
	-c --channel [channel]   Set the listening channel to enumerate the WPS-active APs.
	                         If not set, all channels are listened.
	-P --prompt              If more than one WPS-active AP is found, ask the user [False]
	                         the target to attack.
	-o --output [file]       Outputs all the data into a file.
	-f --pass                If the WPS pin is found, the script uses reaver again to retrieve
	                         the WPA password of the AP.
	-q --quiet               Doesn't print the AP information. Will print the WPS pin and pass if found.
	-F --forever             Runs the program on a While loop so the user can scan and attack a hole
	                         zone without having to execute the program over and over again.
	-O --override            Doesn't prompt the user if the WPS pin of the current AP has already
	                         been found. DOESN'T SKIP THE AP, the script attacks it again.
	                         
#USAGE EXAMPLES

[+] Enumerate the WPS active APs, fetch the AP information with Reaver, use Pixiewps to get the WPS pin, gives wash 15 seconds to search for APs, gives Reaver 6 seconds to fetch the information, uses channel 7, prompt which AP you want to attack, outputs data into a file and tries to get the password running Reaver with the found pin.

	python pyxiewps-[LANGUAGE].py -r -p -w 15 -t 6 -c 7 -P -o file.txt -f
	python pyxiewps-[LANGUAGE].py --use-reaver --use-pixie --wash-time 15 --time 6 --channel 7 --prompt --output file.txt --pass

[+] Same as above but it doesn't prompt for the target, runs in a while loop and override already cracked passwords. This is useful when you try to attack a hole zone as you run the script only once.

	python pyxiewps-[LANGUAGE].py -r -p -w 15 -t 6 -c 7 -F -O -o file.txt -f
	
[+] Only enumerates the WPS acive APs:

	python pyxiewps-[LANGUAGE].py

# Third party bugs 

[+] BE AWARE that some wireless devices are managed by the bcm4313 module. When Pyxiewps tries to bring the iterface up with:
	
	$ ifconfig <interface> up
	
the system crashes leaving the user no other option that bruteforcing a shutdown.
Check your wireless card and then it's module before running this script.

[+] Aircrack sometimes fails to set the interface into monitor mode.
See https://github.com/jgilhutton/pyxiewps#whats-the-aircrack-thing
