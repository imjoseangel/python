#!/usr/bin/python
#-*- Coding: utf-8 -*-

##############################
# Programa que con urllib2 probara una conexion
# a una IP, se podra coger una IP o un rango
# luego en caso de que la conexion sea correcta
# se conectara con selenium y hara un screenshot
# para saber que tiene
##############################

import sys
import os
import threading
import urllib2
import time
#librerias selenium
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#para coger rangos de ips
from netaddr import IPNetwork,IPAddress
#de IPNetwork tendremos que hacer un cast con str, pues esta en bytes
# IPAddress es por si queremos ver si una IP esta en IPNetwork ejemplo: if IPAddress('192.168.1.1') in IPNetwork(subnet)
#subnet para hacer las conexiones
subnet = "192.168.1.0/24" #por defecto
timeout = 1


texto = '''
A long time ago
In a Network far far away
there was a program, wich
allow you to discover
what IPs had a service 
running in the port 80 http
connecting and making a 
screenShot...

This program was written by Fare9 
for educational purposes 
If you are interested, 
you can look at the code freely.
'''

banner = '''
     _______.  ______ .______       _______  _______ .__   __.      _______. __    __    ______   .___________. _______ .______      
    /       | /      ||   _  \     |   ____||   ____||  \ |  |     /       ||  |  |  |  /  __  \  |           ||   ____||   _  \     
   |   (----`|  ,----'|  |_)  |    |  |__   |  |__   |   \|  |    |   (----`|  |__|  | |  |  |  | `---|  |----`|  |__   |  |_)  |    
    \   \    |  |     |      /     |   __|  |   __|  |  . `  |     \   \    |   __   | |  |  |  |     |  |     |   __|  |      /     
.----)   |   |  `----.|  |\  \----.|  |____ |  |____ |  |\   | .----)   |   |  |  |  | |  `--'  |     |  |     |  |____ |  |\  \----.
|_______/     \______|| _| `._____||_______||_______||__| \__| |_______/    |__|  |__|  \______/      |__|     |_______|| _| `._____|           
Version: %s 
Writer: %s 
''' % ('1.3','Fare9')


#Metodo para hacer el intento de conexion:
def tryConnection(IP):
    '''
        Metodo para hacer conexiones con urllib2, 
        miraremos si la IP recibe un response al conectarse, sea cual sea 
    '''
    try:
        if "http" not in str(IP):
            aux = "http://"+str(IP)
        response = urllib2.urlopen(aux,timeout=timeout)
        if len(response.read()) != 0:
            return True
        else:
            return False
    except Exception as e:
        print '[-] ERROR TRYING CONNECT: (%s) %s'%(str(IP),e)
        return False

def screenShot(ImageFolder,IP):
    ''' 
        Metodo para hacer el screenshot con selenium haciendo la conexion
        a la web en caso sea posible esa conexion.
    '''
    IP = str(IP)
    if 'http' not in IP:
        aux = 'http://'+IP 
    #ahora conectar y screenshot
    try:
        if not ImageFolder.endswith('/'):
            nombreScreenShot = ImageFolder+'/'+IP+'.png'
        else:
            nombreScreenShot = ImageFolder+IP+'.png'
        driver = webdriver.Firefox()
        driver.get(aux)
        driver.save_screenshot(nombreScreenShot)
        driver.quit()
    except Exception as e:
        print '[-] ERROR TRYING SCREENSHOT: (%s) %s'%(IP,e)

def main():
    global timeout
    global subnet

    folder = None
    help = '''
        ./IpDetector.py -f <FolderToSaveFiles> -s <SubNet With NetMask> -t <timeout for connections>


        -f:     Folder where you are going to save image files from IPs 
        -s:     Subnet you are going to try to connect.(By Default 192.168.1.0/24)
        -t:     Specify time out connections (by default 1)
        Example:    ./IpDetector.py -f images -s 178.50.40.0/24
    '''
    for index in range(len(sys.argv)):
        if sys.argv[index] == '-f':
            folder = sys.argv[index+1]
        if sys.argv[index] == '-s':
            subnet = sys.argv[index+1]
        if sys.argv[index] == '-t':
            timeout = float(sys.argv[index+1])

    if not folder or not subnet:
        print help
        sys.exit(-1)

    #para ver si existe el directorio y si no lo creo
    if not os.path.exists(folder):
        print '[+] Not folder of name:',folder,'creating, wait a moment...'
        os.makedirs(folder)
        time.sleep(2)

    for ip in IPNetwork(subnet):
        #si es posible conectar...
        print '[+] Trying to connect to:',str(ip)
        if tryConnection(ip):
            t = threading.Thread(target=screenShot,args=(folder,ip))
            t.start()
            #si hemos podido conectar demos tiempo para que se monte el navegador
            time.sleep(5)

if __name__ == '__main__':
    print banner
    print '\n\n Press intro for credits'
    try:
        for c in texto:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.2)
    except KeyboardInterrupt:
        print '... Oh don\'t like my intro?'
        print '[+] Starting Program NOW...'

    main()
