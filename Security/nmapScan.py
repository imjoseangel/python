#!/usr/bin/env python
import nmap
import socket
import optparse

def nmapScan(tgtHost, tgtPort):
	try:
		tgtIP = socket.gethostbyname(tgtHost)
	except:
		print "[-] Cannot resolve '%s': Unknown host" %tgtHost
		return
	
	nmScan = nmap.PortScanner()
	nmScan.scan(tgtIP, tgtPort)
	state = nmScan[tgtIP]['tcp'][int(tgtPort)]['state']
	print " [*] " + tgtHost + " tcp/"+tgtPort +" "+ state

def main():
	parser = optparse.OptionParser('Usage: %prog -H <target host> -p <target port>')
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma')
	(options, args) = parser.parse_args()

	if (options.tgtHost == None) | (options.tgtPort == None):
		print parser.usage
		exit(0)
	else:
		tgtHost = options.tgtHost
		tgtPorts = str(options.tgtPort).split(',')

	for tgtPort in tgtPorts:
		nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
	main()
