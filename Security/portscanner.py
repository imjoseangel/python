#!/usr/bin/env python

import optparse
import socket
from threading import *

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
	try:
		connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send('GET\r\n')
		results = connSkt.recv(100)
		screenLock.acquire()
		print '[+] %d/tcp open'% tgtPort
		print '[+] ' + str(results)
	except Exception, e:
		screenLock.acquire()
		print '[-]%d/tcp closed'% tgtPort
		print e
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost, tgtPorts):
	try:
		tgtIP = socket.gethostbyname(tgtHost)
	except:
		print "[-] Cannot resolve '%s': Unknown host" %tgtHost
		return
	try:
		tgtName = socket.gethostbyaddr(tgtIP)
		print '\n[+] Scan Results for: ' + tgtName[0]
	except:
		print '\n[+] Scan Results for: ' + tgtIP

	socket.setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
		t.start()

def main():
	parser = optparse.OptionParser("%prog -H <target host> -p <target port>")
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma')

	(options, args) = parser.parse_args()

	if (options.tgtHost == None) | (options.tgtPort == None):
		print parser.usage
		exit(0)
	else:
		tgtHost = options.tgtHost
		tgtPorts = str(options.tgtPort).split(",")

	portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
	main()
