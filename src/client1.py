import os
from classes import *
import cfunctions
from functions import *

ip = raw_input('Ingrese el IP del servidor: ')
port = raw_input('Ingrese el puerto del servidor: ')
petition = serverPetition(0, os.getpid(), 'Petition Body', ip, int(port))
cfunctions.sendPetition(0, os.getpid(), toJson(petition), ip, int(port))

#10.6.0.219