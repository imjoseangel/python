#!/usr/bin/env python
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = 'localhost'
port_number = 9999
my_socket.bind((hostname, port_number))
my_socket.listen(5)

while True:
	#now we wait accept the client
	#connection and address are new variables
	connection, address = my_socket.accept()
	#after we accept the connection we inform the client: you connected
	#we use the send method
	connection.send("you connected")
	
