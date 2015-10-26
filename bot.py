# -*- coding: utf-8 -*-
import subprocess
import re
import urllib
import urllib2
import json
import os
import imghdr

import telebot                  # Libreria de la API del bot.
from telebot import types       # Tipos para la API del bot.
import time                     # Libreria para hacer que el programa que controla el bot no se acabe.
from config import token        # Libreria de configuracion
import sys
from collections import OrderedDict
import random

##
reload(sys)                     # Forzamos UTF-8 para que no de excepcion
sys.setdefaultencoding("utf-8") #  si llega algun caracter especial
##

bot = telebot.TeleBot(token)     # Creamos el objeto de nuestro bot.


usuarios = [line.rstrip('\n') for line in open('usuarios.txt')] # Cargamos la lista de usuarios.


#############################################
#           Textos
#############################################
normas = OrderedDict([
    ('1', 'No hacer flood'),
    ('2', 'No hacer spam'),
    ('3', '/info para ver los posibles comandos')
    ])

comandos = OrderedDict([
    ('/normas', 'Normas del grupo'),
    ('/info', 'Informacion del grupo'),
    ('/insultame', 'Insulto gratuito de regalo')
    ])

#############################################
#               Listener
#############################################
def listener(messages):                             # Con esto, estamos definiendo una funcion llamada 'listener', que recibe como parametro un dato llamado 'messages'.
    for m in messages:                              # Por cada dato 'm' en el dato 'messages'
        cid = m.chat.id                             # Almacenaremos el ID de la conversacion.
        if m.content_type == 'text':                # Si es texto, guardamos el comando en el log  
            if cid > 0:
                mensaje = str(m.chat.first_name) + " [" + str(cid) + "]: " + m.text
            else:
                mensaje = str(m.from_user.first_name) + "[" + str(cid) + "]: " + m.text            
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
            print mensaje
        #elif m.content_type == 'new_chat_participant':
        #    if cid == grupo:
        #        bot.send_message( cid, 'Bienvenido, echale un vistazo a las normas :)')
        #        command_normas(m)
        #elif m.content_type == 'left_chat_participant':
        #    if cid == grupo:
        #        bot.send_sticker( cid, open( 'adios.webp', 'rb'), reply_to_message_id=int(m.message_id))

bot.set_update_listener(listener)                   # Asi, le decimos al bot que utilice como funcion escuchadora nuestra funcion 'listener' declarada arriba.


#############################################
#               Funciones
#############################################
#@bot.message_handler(commands=['roto2'])                # Indicamos que lo siguiente va a controlar el comando '/roto2'.
#def command_roto2(m):                                   # Definimos una funcion que resuelva lo que necesitemos.
#    cid = m.chat.id                                     # Guardamos el ID de la conversacion para poder responder.
#    bot.send_photo( cid, open( 'roto2.png', 'rb'))      # Con la funcion 'send_photo()' del bot, enviamos al ID de la conversacion que hemos almacenado previamente la foto de nuestro querido :roto2:
 
@bot.message_handler(commands=['insultame']) 
def command_insultame(m): 
    cid = m.chat.id # Guardamos el ID de la conversaci?n para poder responder.
    numero = random.randrange(20) 
    frases ={1:"estupido!",
     2:"Imbecil!",
     3:"Asqueroso",
     4:"Gilipollas!",
     5:"Muerdealmohadas!",
     6:"Vete a tomar por culo",
     7:"Hijo de puta!",
     8:"Abrazafarolas",
     9:"Payaso de mierda!",
    10:"Abrazapinos",
    11:"Comeflores",
    12:"Que apropiado, tu peleas como una vaca",
    13:"Yo soy cola, tu pegamento..",
    14:"Tu mas...",
    15:"Vacaburro",
    16:"Me cago en tu cabeza",
    17:"Cenutrio",
    18:"Zote",
    19:"Eres tan tonto que te tendr?an que dar 2 medallas, una por tonto y otra por si la pierdes",
    20:"Eres la mejor prueba de que Dios realmente tiene sentido del humor",
    21:"Te diferencias de los caballos en una sola neurona, lo justo como para no cagarte en los desfiles"
     }
    mensaje = frases[numero]
    bot.send_message( cid, mensaje)

@bot.message_handler(commands=['normas'])
def command_normas(m):
    cid = m.chat.id
    mensaje = 'Normas:\n'
    for a,b in normas.iteritems():
        mensaje += a + ') ' + b + '\n'
    bot.send_message( cid, mensaje)
    print "Enviando normas..."

@bot.message_handler(commands=['info'])
def command_info(m):
    cid = m.chat.id
    mensaje = 'Comandos posibles:\n'
    for a,b in comandos.iteritems():
        mensaje += a + ' ' + b + '\n'
    bot.send_message( cid, mensaje)
    print "Enviando ayuda..."
#
#@bot.message_handler(commands=['rae'])
#def command_rae(m):
#      cid = m.chat.id
#      msg = m.text[5:]
#      link = urllib.urlopen("http://dulcinea.herokuapp.com/api/?query=" + msg)
#      data = json.loads(link.read())
#      for r in data['response']:
#            if 'meanings' in r:
#                bot.send_message(cid, data["response"][0]["meanings"][0]["meaning"])
#                bot.send_message(cid, data["response"][1]["meanings"][0]["meaning"])
#                break;
#            else:
#                bot.send_message(cid, "Error en la busqueda")

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if not str(cid) in usuarios:                        # Con esta sentencia, hacemos que solo se ejecute lo de abajo cuando un usuario hace uso del bot por primera vez.
        usuarios.append(str(cid))                       # En caso de no estar en la lista de usuarios, lo anadimos.
        aux = open( 'usuarios.txt', 'a')                # Y lo insertamos en el fichero 'usuarios.txt'
        aux.write( str(cid) + "\n")
        aux.close()
        bot.send_message( cid, "Bienvenido al bot!!!!")

        comando = m.text[7:]
        if comando == 'normas':
            command_normas(m)
        elif comando == 'info':
            command_info(m)
        elif comando == 'insultame':
            command_insultame(m)
        elif comando == 'img':
            command_img(m)

@bot.message_handler(commands=['df'])
def command_df(m):
    cid = m.chat.id
    
    #p = subprocess.Popen("df -h", stdout=subprocess.PIPE, shell=True)
    #dfdata, _ = p.communicate()
    #dfdata = dfdata.replace("Mounted on", "Mounted_on")
    #
    #mensaje = [list() for i in range(10)]
    #for line in dfdata.split("\n"):
    #    line = re.sub(" +", " ", line)
    #    for i,l in enumerate(line.split(" ")):
    #        mensaje[i].append(l)
    
    import os, re
    mensaje =''
    l=[]
    p=os.popen('df -h')
    for line in p.readlines():
        if line.startswith("/"):
            values = line.split()
            mensaje += values[5]+ "\t" + values[4]+ "\t"  + values[3] + '\n'
    p.close()
    bot.send_message( cid, mensaje)
    
@bot.message_handler(commands=['imdb'])
def command_imdb(m):
    cid = m.chat.id
    texto = m.text[6:]
    url = "http://www.omdbapi.com/?t=%s&y=&plot=short&r=json" % texto
    link = urllib.urlopen(url)
    data = json.loads(link.read())
    if data['Response'] == 'False':
        bot.send_message(cid, 'Pelicula no encontrada')
    
    image = urllib.URLopener()
    print "data poster: %s" % data['Poster']
    if data['Poster'] != 'N/A':
        image.retrieve(data['Poster'], "imdb_tmp.jpg")
        bot.send_photo(cid, open( 'imdb_tmp.jpg', 'rb'))
    results = """*Titulo*: """ + data['Title'] + "\n" + """*Rating*: """ + "\n" +data['imdbRating'] + "\n" """*Argumento*: """ + data['Plot']
    bot.send_message(cid, results, parse_mode="Markdown")


@bot.message_handler(commands=['img'])
def command_img(m):
    cid = m.chat.id
    texto = m.text[5:]
    texto.encode('utf-8')
    
    RandStart = random.randint(0, 50)
    url = 'http://ajax.googleapis.com/ajax/services/search/images?&v=1.0'
    url += '&rsz=8'
    url += '&start='+ str(RandStart)
    url += '&fileType=jpg'
    url += '&imgsz=medium'
    url += '&q=' + texto.replace(' ', '%20')
    print url
    f = urllib2.urlopen(url)
    data = json.load(f)
    f.close()
    results = data['responseData']['results']
    url = results[random.randint(0, len(results) - 1)]['url']
    urllib.urlretrieve(url, './image.jpg')
    #imagetype = imghdr.what('./image')
    #if not(type(imagetype) is None):
        #os.rename('./image', './image.jpg' + imagetype)
    
    #bot.send_photo(cid, open( './image.' + imagetype, 'rb'))
    bot.send_photo(cid, open( './image.jpg'))


#############################################
#           Peticiones
#############################################
bot.polling(none_stop=True)                             # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.


